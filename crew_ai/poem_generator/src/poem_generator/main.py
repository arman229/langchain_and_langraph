import random
from pydantic import BaseModel
from crewai.flow.flow import listen, start, Flow
from poem_generator.crews.poem_generator import PoemCrew

class PoemClass(BaseModel):
    sentence_count: int = 2
    poem: str = ""
    translated_poem: str = ""

class FinalPoem(Flow[PoemClass]):
    
    @start()
    def generate_sentence_count(self):
        print("Generating sentence count")
        no_of_sentences = random.randint(1, 6)
        self.state.sentence_count = no_of_sentences
        print(f"Sentence count: {self.state.sentence_count}")
        
    @listen(generate_sentence_count)
    def generate_final_poem(self):
        print("Generating final poem")
        resp = PoemCrew().crew().kickoff(inputs={'sentence_count': self.state.sentence_count})
        print(f"Poem: {resp.raw}")
        self.state.poem = resp.raw
                
    

    @listen(generate_final_poem)
    def save_poem(self):
        print("Saving poems")
        with open('poem.txt', 'w', encoding='utf-8') as f:
            f.write("Original Poem:\n")
            f.write(self.state.poem + "\n\n")
       
            
def kickoff():
    final_poem_flow = FinalPoem()
    final_poem_flow.kickoff()
    
def plot():
    final_poem_flow = FinalPoem()
    final_poem_flow.plot()
