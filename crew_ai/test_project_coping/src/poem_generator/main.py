import random
from pydantic import BaseModel
from crewai.flow.flow import listen, start, Flow
from poem_generator.crews.poem_generator import Personal_crew
from poem_generator.crews.tool_agent import crew


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
    final_poem_flow = FinalAns()
    final_poem_flow.kickoff()


def plot():
    final_poem_flow = FinalAns()
    final_poem_flow.plot()
