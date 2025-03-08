import random
from pydantic import BaseModel
from crewai.flow.flow import listen, start, Flow
from poem_generator.crews.poem_generator import Personal_crew 

 
class FinalAns(Flow ):
    
    @start()
    def generate_sentence_count(self): 
          
        resp = Personal_crew().crew().kickoff(inputs={"question": "Who Muhammad Qasim and where he live"})
        print(f"final_resp: {resp.raw}")
        
        
 
                
    

 
       
            
def kickoff():
    final_poem_flow = FinalAns()
    final_poem_flow.kickoff()
    
def plot():
    final_poem_flow = FinalAns()
    final_poem_flow.plot()
