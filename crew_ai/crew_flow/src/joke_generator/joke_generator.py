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
        print(f'api keys :{self.API_KEY}')
        messages = [{"role": "user", "content": "Please generate a whole number between 1 to 5 randomly. "}]
        response = completion(api_key=self.API_KEY,model=self.model, messages=messages)
        result = response['choices'][0]['message']['content']
        print(result)
        return result
    
    @listen(no_of_jokes)
    def generate_jokes(self,no_of_jokes):
        messages = [{"role": "user", "content": f"Generate {no_of_jokes} jokes."}]
        response = completion(api_key=self.API_KEY,model=self.model, messages=messages)
        result = response['choices'][0]['message']['content']
        print(result)
        return result
        
        
    @listen(generate_jokes)
    def best_jokes(self,jokes):
        messages = [{"role": "user", "content": f"Here is a list of jokes: {jokes}. Please select the best 1 joke."}]
        response = completion(api_key=self.API_KEY,model=self.model, messages=messages)
        result = response['choices'][0]['message']['content']
        print(result)
        return result
      
      
  
def jokegenerator():
    joke_class =  JokeGenerator()       
    resp = joke_class.kickoff()
    print(resp)