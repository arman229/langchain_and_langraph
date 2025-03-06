from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os 
from crewai import LLM
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = os.environ.get("MODEL")

localllm = LLM(model="ollama/deepseek-r1:1.5b", base_url="http://localhost:11434")

# gemini_llm = LLM(
#     model=MODEL,
#     api_key=GEMINI_API_KEY,
#     temperature=0,
# )

@CrewBase
class PoemCrew: 
    agents_config = 'configs/agents.yaml'   
    tasks_config = 'configs/tasks.yaml'    

    @agent
    def poem_writer(self) -> Agent:
        return Agent(config=self.agents_config['poem_writer'], llm=localllm)
    
   
    @task
    def write_poem(self) -> Task:
        return Task(config=self.tasks_config['write_poem'])
    
   
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,   
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
