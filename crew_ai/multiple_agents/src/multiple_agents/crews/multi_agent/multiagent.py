from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os 

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = os.environ.get("MODEL")

gemini_llm = LLM(
    model=MODEL,
    api_key=GEMINI_API_KEY,
    temperature=0,
)
@CrewBase
class MultiAgent: 
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml" 
    @agent
    def question_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["question_generator"], llm=gemini_llm
        )
 
    @task
    def generate_questions(self) -> Task:
        return Task(
            config=self.tasks_config["generate_questions"],
        )
        
    @agent
    def answer_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["answer_generator"], llm=gemini_llm
        )
 
    @task
    def generate_answers(self) -> Task:
        return Task(
            config=self.tasks_config["generate_answers"],
        )

    @crew
    def crew(self) -> Crew: 

        return Crew(
            agents=self.agents,  
            tasks=self.tasks,   
            process=Process.sequential,
            verbose=True,
        )
