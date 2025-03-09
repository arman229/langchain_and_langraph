from crewai import Agent, Task, Crew 
from  memory_and_external_tools.crews.custom_tools import PiaicCardInputSchema,my_tool 
from  memory_and_external_tools.crews.first_crew import gemini_llm
card = PiaicCardInputSchema()


piaic_manager = Agent(
    role="PIAIC manager",
    goal = "Manage all quries regarding PIAIC and you will use only relevant tools for student query",
    backstory="""You are a master at understanding people and their preferences.""",
    tools=[card, my_tool],
    verbose=True,
    llm=gemini_llm
)

piaic_card_creator = Task(
    description="you will be responsible for all PIAIC relevant operations, student query '{query}' you must be know how to answer his question based on final context",
    expected_output="final query answer only",
    agent=piaic_manager
)

crew = Crew(
    agents=[piaic_manager],
    tasks=[piaic_card_creator],
    verbose=True
)

