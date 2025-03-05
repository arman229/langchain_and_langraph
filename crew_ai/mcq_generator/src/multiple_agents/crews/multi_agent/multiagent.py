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
    def qa_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["qa_generator"], llm=gemini_llm
        )
 
    @task
    def task_qa_generator(self) -> Task:
        return Task(
            config=self.tasks_config["task_qa_generator"],
        )
        
 
    @crew
    def crew(self) -> Crew: 

        return Crew(
            agents=self.agents,  
            tasks=self.tasks,   
            process=Process.sequential,
            verbose=True,
        )
