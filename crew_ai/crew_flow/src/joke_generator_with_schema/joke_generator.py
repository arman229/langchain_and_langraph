from crewai.flow.flow import start,listen,Flow
from litellm import completion
import json
from dotenv import load_dotenv
load_dotenv()
import os 
 
class JokeGenerator(Flow):
    model = os.getenv("GEMINI_MODEL","gemini/gemini-1.5-flash" )   
    API_KEY = os.getenv("GEMINI_API_KEY") 
 
    
    @start()
    def no_of_jokes(self):  
        messages = [{"role": "user", "content": "Please generate a whole number between 1 to 5 randomly. "}]
        response = completion(api_key=self.API_KEY,model=self.model, messages=messages)
        result = response['choices'][0]['message']['content']
        print(result)
        self.state['total_jokes'] = result
    
    @listen(no_of_jokes)
    def generate_jokes(self):
        messages = [{"role": "user", "content": f"Generate {self.state['total_jokes']} jokes."}]
        response = completion(api_key=self.API_KEY,model=self.model, messages=messages)
        result = response['choices'][0]['message']['content']
        print(result)
        self.state['joke_list'] = result
        
        
    @listen(generate_jokes)
    def best_jokes(self):
        messages = [{"role": "user", "content": f"Here is a list of jokes: {self.state['joke_list']}. Please select the best 1 joke."}]
        response = completion(api_key=self.API_KEY,model=self.model, messages=messages)
        result = response['choices'][0]['message']['content']
        print(result) 
      
      
  
def jokegenerator():
    joke_class =  JokeGenerator()       
    resp = joke_class.kickoff()
    print(resp)