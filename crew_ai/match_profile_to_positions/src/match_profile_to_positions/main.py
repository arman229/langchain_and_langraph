#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from match_profile_to_positions.crews.read_cv_crew.read_cv import ReadCvCrew


 

class MatchProfilePositionFlow(Flow):

    @start()
    def cv_reader_fun(self):
        inputs = {"cv_path": "./src/match_profile_to_positions/crews/read_cv_crew/data/cv.md"}  
        crew = ReadCvCrew().crew().kickoff(inputs=inputs)
        crew.run()

 


def kickoff():
    resp = MatchProfilePositionFlow()
    resp.kickoff()


def plot():
    resp = MatchProfilePositionFlow()
    resp.plot()



 