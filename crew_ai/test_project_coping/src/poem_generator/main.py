import random
from pydantic import BaseModel
from crewai.flow.flow import listen, start, Flow
from poem_generator.crews.poem_generator import Personal_crew
from poem_generator.crews.tool_agent import crew

from poem_generator.crews.read_cv_crew.read_cv import ReadCvCrew
class MatchProfilePositionFlow(Flow):

    @start()
    def cv_reader_fun(self):
        inputs = {"cv_path": "./src/poem_generator/crews/read_cv_crew/data/cv.md"}
        print('hi')
        crew = ReadCvCrew().crew().kickoff(inputs=inputs)
        print('crew final result is:',crew.raw)

 


def kickoff():
    resp = MatchProfilePositionFlow()
    resp.kickoff()


def plot():
    resp = MatchProfilePositionFlow()
    resp.plot()




# class FinalAns(Flow):

#     @start()
#     def generate_sentence_count(self):

#         resp = crew.kickoff(
#             inputs={
#                 "query": "hi i am arman"
#             }
#         )
#         print(f"final_resp: {resp.raw}")


# def kickoff():
#     final_poem_flow = FinalAns()
#     final_poem_flow.kickoff()


# def plot():
#     final_poem_flow = FinalAns()
#     final_poem_flow.plot()
