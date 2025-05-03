from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
from crewai_tools import CSVSearchTool, FileReadTool
gemini_llm = LLM(model=os.getenv("MODEL_NAME"), api_key=os.getenv("GEMINI_API_KEY"))
os.environ["OPENAI_API_KEY"] = "fake-key"

google_embedder = {
    "provider": "google",
    "config": {
         "model": "models/text-embedding-004",
         "api_key": os.getenv('GEMINI_API_KEY'),
         }
}

@CrewBase
class SingleCvCrewNew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def cv_reader(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_reader"],
            tools=[FileReadTool()],
            llm=gemini_llm, 
            verbose=True,
            allow_delegation=False,
        )

    @task
    def read_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config['read_cv_task'], 
            agent=self.cv_reader(),
            
        )
    
    @agent
    def matcher(self) -> Agent:
            return Agent(
                    config=self.agents_config['matcher'],
                    tools=[FileReadTool(), CSVSearchTool()],
                    llm=gemini_llm, 
                    verbose=True,
                    allow_delegation=False
            )
    @task
    def match_cv_task(self) -> Task:
            return Task(
                    config=self.tasks_config['match_cv_task'],
                    agent=self.matcher()
            )
    
    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True, 
            embedder=google_embedder
        )

 