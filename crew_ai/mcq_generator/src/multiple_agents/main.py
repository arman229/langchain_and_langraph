from crewai.flow.flow import Flow, start, listen
import re
import json

from random import randint

from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from multiple_agents.crews.multi_agent.multiagent import MultiAgent
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib import colors
import json


def convert_superscripts(text):
    """
    Convert any Unicode superscript characters into ReportLab's <super> markup.
    This will handle any sequence of superscript characters.
    """
    pattern = r"([⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ]+)"
    mapping = {
        "⁰": "0",
        "¹": "1",
        "²": "2",
        "³": "3",
        "⁴": "4",
        "⁵": "5",
        "⁶": "6",
        "⁷": "7",
        "⁸": "8",
        "⁹": "9",
        "⁺": "+",
        "⁻": "-",
        "⁼": "=",
        "⁽": "(",
        "⁾": ")",
        "ⁿ": "n",
    }

    def replacer(match):
        sup_seq = match.group(1)
        converted = "".join(mapping.get(ch, ch) for ch in sup_seq)
        return f"<super>{converted}</super>"

    return re.sub(pattern, replacer, text, flags=re.DOTALL)


class AgentState(BaseModel):
    no_of_questions: int = 10
    topic: str = ""
    question_paper: list[dict] = []  # List of question dictionaries


class AgentFlow(Flow[AgentState]):
    @start()
    def no_of_questions(self):
        print("Setting up the task...")
        self.state.no_of_questions = 200
        self.state.topic = "General Math"  # or your desired topic

    @listen(no_of_questions)
    def generate_questions(self):
        print("Generating questions...")
        required = self.state.no_of_questions
        unique_questions = []  # Global collection of unique questions
        seen = set()  # Set to hold normalized question text for duplicate checking

        def normalize(q_text):
            return q_text.strip().lower()

        iteration = 0
        window_context_size = (
            40  # how many questions to request in one batch (you mentioned 40)
        )

        # Continue generating until we have the required number of unique questions.
        while len(unique_questions) < required:
            iteration += 1
            batch_size = min(window_context_size, required - len(unique_questions))
            # Include an iteration-specific hint to force uniqueness
            result = (
                MultiAgent()
                .crew()
                .kickoff(
                    inputs={
                        "no_of_questions": batch_size,
                        "topic": self.state.topic,
                        "unique_hint": f"Iteration {iteration}: Please generate {batch_size} new, unique, and challenging MCQs that have not been generated in previous iterations.",
                    }
                )
            )
            raw_result = result.raw
            # Remove markdown markers if present
            lines = raw_result.splitlines()
            if lines and lines[0].startswith("```json"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            raw_json = "\n".join(lines)

            try:
                batch_data = json.loads(raw_json)
            except json.JSONDecodeError as e:
                print("Error parsing batch JSON:", e)
                continue

            # If batch_data is nested (list of lists), flatten it.
            if batch_data and isinstance(batch_data[0], list):
                flat_batch = []
                for sublist in batch_data:
                    flat_batch.extend(sublist)
                batch_data = flat_batch

            # Filter out duplicates in the batch based on normalized question text.
            new_questions = []
            for item in batch_data:
                q_norm = normalize(item.get("question", ""))
                if q_norm not in seen:
                    seen.add(q_norm)
                    new_questions.append(item)
                else:
                    print(f"Duplicate found (ignored): {item.get('question')}")

            unique_questions.extend(new_questions)
            print(
                f"Iteration {iteration}: Generated {len(new_questions)} unique questions. Total unique so far: {len(unique_questions)}"
            )

        # If more than required were generated, trim the list.
        self.state.question_paper = unique_questions[:required]
        print(
            "Final unique question paper generated with",
            len(self.state.question_paper),
            "questions.",
        )

    @listen(generate_questions)
    def save_question_paper(self):
        # Convert superscripts for each text field in every question dictionary.
        def convert_question_dict(item):
            item["question"] = convert_superscripts(item["question"])
            item["options"] = [convert_superscripts(opt) for opt in item["options"]]
            item["answer"] = convert_superscripts(item["answer"])
            item["explanation"] = convert_superscripts(item["explanation"])
            return item

        mockdata = [
            {
                "question": "What is the derivative of f(x) = 3x² - 4x + 6?",
                "options": ["6x - 4", "3x - 4", "6x² - 4", "9x - 4"],
                "answer": "6x - 4",
                "explanation": "The power rule of differentiation states that the derivative of xⁿ is nxⁿ⁻¹. Applying this rule to each term: the derivative of 3x² is 6x, the derivative of -4x is -4, and the derivative of a constant (6) is 0. Therefore, the derivative of f(x) is 6x - 4.",
            }
        ]
        # Process each question dictionary in the question paper.
        data = [convert_question_dict(item) for item in self.state.question_paper]
        print(f'data:{data}')
        print(f'mockdata:{mockdata}')
        datas = [convert_question_dict(item) for item in mockdata]
        print(f'data:{datas}')
        
        print(f"Saving question paper with {len(data)} questions...")
        pdf_filename = "question_paper1.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=A4)

        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        question_style = ParagraphStyle(
            "QuestionStyle",
            parent=styles["Normal"],
            fontSize=12,
            textColor=colors.black,
            spaceAfter=8,
            leading=14,
        )
        option_style = ParagraphStyle(
            "OptionStyle",
            parent=styles["Normal"],
            fontSize=11,
            textColor=colors.darkgreen,
            leftIndent=20,
            spaceAfter=4,
        )
        answer_style = ParagraphStyle(
            "AnswerStyle",
            parent=styles["Normal"],
            fontSize=11,
            textColor=colors.darkblue,
            leftIndent=20,
            spaceAfter=6,
        )
        explanation_style = ParagraphStyle(
            "ExplanationStyle",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.grey,
            leftIndent=40,
            spaceAfter=12,
        )

        def extract_code(question_text):
            code_pattern = r"```python\s*([\s\S]*?)\s*```"
            match = re.search(code_pattern, question_text)
            if match:
                code = match.group(1).strip()
                cleaned_question = re.sub(code_pattern, "", question_text).strip()
                return code, cleaned_question
            return None, question_text

        elements = []
        elements.append(Paragraph("Generated Question Paper", title_style))
        elements.append(Spacer(1, 12))

        for i, item in enumerate(data, start=1):
            code_snippet, cleaned_question = extract_code(item["question"])
            elements.append(Paragraph(f"{i}. {cleaned_question}", question_style))
            if code_snippet:
                elements.append(Preformatted(code_snippet, styles["Code"]))
                elements.append(Spacer(1, 6))
            for idx, option in enumerate(item["options"], start=1):
                elements.append(Paragraph(f"{chr(96 + idx)}) {option}", option_style))
            elements.append(Paragraph(f"✅ Answer: {item['answer']}", answer_style))
            elements.append(
                Paragraph(f"💡 Explanation: {item['explanation']}", explanation_style)
            )
            elements.append(Spacer(1, 12))

        doc.build(elements)
        print(f"\n🎉 PDF saved successfully as '{pdf_filename}'")


def kickoff():
    agent_flow = AgentFlow()
    agent_flow.kickoff()


def plot():
    agent_flow = AgentFlow()
    agent_flow.plot()
