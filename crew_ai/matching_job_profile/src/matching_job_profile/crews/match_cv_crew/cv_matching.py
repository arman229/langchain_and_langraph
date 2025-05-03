from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os

gemini_llm = LLM(model= 'gemini/gemini-1.5-flash', api_key=os.getenv("GEMINI_API_KEY"))


@CrewBase
class MatchCvCrewNew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def cv_matcher(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_matcher"],
            llm=gemini_llm,
            verbose=True,
            allow_delegation=False,
        )

    @task
    def match_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config['match_cv_task'], 
           
        )

    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
