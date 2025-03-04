#!/usr/bin/env python
from random import randint

from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from  multiple_agents.crews.multi_agent.multiagent import MultiAgent
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib import colors
import json

class AgentState(BaseModel):
    no_of_questions: int = 1
    topic: str = ""
    question_paper: list[str] = [] 

class AgentFlow(Flow[AgentState]):

    @start()
    def no_of_questions(self):
        print("Generating no of questions...")
        self.state.no_of_questions = randint(100, 101)

    @listen(no_of_questions)
    def generate_questions(self):
        print("Generating questions...")
        result = (
            MultiAgent()
            .crew()
            .kickoff(inputs={"no_of_questions": self.state.no_of_questions, "topic": 'Python'})
        )

        print("Questions generated", result.raw)
        self.state.question_paper = result.raw



    @listen(generate_questions)
    def save_question_paper(self):
        print(f"Saving question paper... {self.state.question_paper}")
    
        raw_result = self.state.question_paper
        
        lines = raw_result.splitlines()
        if lines[0].startswith("```json"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        raw_json = "\n".join(lines)
        def escape_newlines_in_json(json_str):
            
            pattern = r'("((?:\\.|[^"\\])*)")'
            def replacer(match):
                full_match = match.group(1)
                inner_text = match.group(2) 
                escaped_text = inner_text.replace("\n", "\\n")
                return f'"{escaped_text}"'
            return re.sub(pattern, replacer, json_str, flags=re.DOTALL)

        escaped_json = escape_newlines_in_json(raw_json)
        
        try:
            data = json.loads(escaped_json) 
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
        pdf_filename = "question_paper.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
        
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        question_style = ParagraphStyle(
            "QuestionStyle",
            parent=styles["Normal"],
            fontSize=12,
            textColor=colors.black,
            spaceAfter=8,
            leading=14
        )
        option_style = ParagraphStyle(
            "OptionStyle",
            parent=styles["Normal"],
            fontSize=11,
            textColor=colors.darkgreen,
            leftIndent=20,
            spaceAfter=4
        )
        answer_style = ParagraphStyle(
            "AnswerStyle",
            parent=styles["Normal"],
            fontSize=11,
            textColor=colors.darkblue,
            leftIndent=20,
            spaceAfter=6
        )
        explanation_style = ParagraphStyle(
            "ExplanationStyle",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.grey,
            leftIndent=40,
            spaceAfter=12
        )

        
        def extract_code(question_text):
            code_pattern = r"```python\s*([\s\S]*?)\s*```"   
            match = re.search(code_pattern, question_text)
            
            if match:
                code = match.group(1).strip()   
                cleaned_question = re.sub(code_pattern, "", question_text).strip()  # Remove code block from question
        
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
        
            elements.append(Paragraph(f"💡 Explanation: {item['explanation']}", explanation_style))
        
            elements.append(Spacer(1, 12)) 
        doc.build(elements)

        print(f"\n🎉 PDF saved successfully as '{pdf_filename}'")


def kickoff():
    poem_flow = AgentFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = AgentFlow()
    poem_flow.plot()


 