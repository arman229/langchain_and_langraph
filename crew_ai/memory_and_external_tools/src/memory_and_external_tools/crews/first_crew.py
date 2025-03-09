from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
from crewai import LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from crewai import Crew, Process
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory.storage.rag_storage import RAGStorage
from typing import List, Optional
from mem0 import MemoryClient
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

MEMO_API_KEY = os.environ.get("MEMO_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = os.environ.get("MODEL", "gemini/gemini-1.5-flash")
client = MemoryClient(api_key=MEMO_API_KEY)
gemini_llm = LLM(
    model=MODEL,              
    api_key=GEMINI_API_KEY,
    temperature=0,
)
google_embedder = {
    "provider": "google",
    "config": {
        "model": "models/embedding-001",
        "api_key": GEMINI_API_KEY,
    },
}

content = "Hi, I'm arman . I am a student of PIAIC . I want to become a world level AI developer .I am from pakistan"
string_source = StringKnowledgeSource(
    content=content,
)


@CrewBase
class Personal_crew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def personal_agent(self) -> Agent:
        return Agent(config=self.agents_config["personal_agent"], llm=gemini_llm)

    @task
    def personal_agent_task(self) -> Task:
        return Task(config=self.tasks_config["personal_agent_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            
            agents=self.agents,
            tasks=self.tasks,
            memory=True,
            # Long-term memory for persistent storage across sessions
            # long_term_memory=LongTermMemory(
            #     storage=LTMSQLiteStorage(
            #         db_path="./my_crew2/long_term_memory_storage1.db"
            #     )
            # ),
            # # # Short-term memory for current context using RAG
            # short_term_memory=ShortTermMemory(
            #     storage=RAGStorage(
            #         embedder_config=google_embedder,
            #         type="short_term",
            #         path="./my_crew2/short_term1/",
            #     )
            # ),
            # # Entity memory for tracking key information about entities
            # entity_memory=EntityMemory(
            #     storage=RAGStorage(
            #         embedder_config=google_embedder,
            #         type="short_term",
            #         path="./my_crew2/entity1/",
            #     )
            # ),
            verbose=True,
            process=Process.sequential,
            knowledge_sources=[string_source],
            embedder=google_embedder,
            memory_config={
                "provider": "mem0",
                "config": {"user_id": "john","api_key": MEMO_API_KEY },
            },
        )
