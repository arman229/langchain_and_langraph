from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os

gemini_llm = LLM(model=os.getenv("MODEL_NAME"), api_key=os.getenv("GEMINI_API_KEY"))


@CrewBase
class ReadCvCrewNew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def cv_reader(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_reader"],
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

    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
