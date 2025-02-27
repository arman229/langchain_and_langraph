
from crewai.flow.flow import Flow,start, listen

    
class SimpleFlow(Flow):
    
    @start()
    def start(self):
        print('start')
    
    @listen(start)
    def afterstart(self):
        print('after start')
                     
def crewfun(): 
    flow = SimpleFlow()
    final_resp = flow.kickoff()                   
    # print(final_resp)