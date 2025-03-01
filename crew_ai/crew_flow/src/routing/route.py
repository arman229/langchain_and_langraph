from crewai.flow.flow import start,listen, Flow,router
from litellm import completion
from pydantic import BaseModel
import random

class Route(BaseModel):
    flag:bool = False
    
    
class  Routeclass(Flow[Route]):
    
    @start()
    def starterfun(self):
        current_choice = random.choice([False,True])
        print(f'Current choice: {current_choice}')
        self.state.flag = current_choice
        
    @router(starterfun) 
    def routerfun(self):
        if self.state.flag:
            print('Flag is True')
            return 'success'
        else:
            print('Flag is False') 
            return 'failure'
        
    @listen('success') 
    def successfun(self):
        print('Success function')

    @listen('failure') 
    def failurefun(self):
        print('failure function')
        
        
def finalroutes():
    route_class = Routeclass()
    route_class.kickoff()        
    
    
def finalroutesplot():
    route_class = Routeclass()
    route_class.plot()        