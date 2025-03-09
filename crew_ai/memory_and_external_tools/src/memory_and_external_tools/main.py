import random
from pydantic import BaseModel
from crewai.flow.flow import listen, start, Flow
from memory_and_external_tools.crews.tool_agent import crew
from memory_and_external_tools.crews.first_crew import Personal_crew


class FinalAns(Flow):

    @start()
    def generate_sentence_count(self):

        resp = crew.kickoff(
            inputs={
                "query": "hi i am arman"
            }
        )
        print(f"final_resp: {resp.raw}")


def kickoff():
    final_flow = FinalAns()
    final_flow.kickoff()


def plot():
    final_flow = FinalAns()
    final_flow.plot()
