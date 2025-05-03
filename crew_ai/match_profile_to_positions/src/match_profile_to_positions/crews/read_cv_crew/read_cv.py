from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import   FileReadTool
 
@CrewBase
class ReadCvCrew: 
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml" 
    @agent
    def cv_reader_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_reader_agent"],
            tools=[FileReadTool()],
            verbose=True,
            allow_delegation=False,
        )
 
    @task
    def cv_reader_task(self) -> Task:
        return Task(
            config=self.tasks_config["cv_reader_task"],
        )

    @crew
    def crew(self) -> Crew: 

        return Crew(
            agents=self.agents,   
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
