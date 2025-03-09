from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from crewai.tools import tool
from poem_generator.crews.poem_generator import gemini_llm
 
class CardInputSchema(BaseModel):
    student_name: str = Field(..., title="Student Name", description="Enter Student Name")
    student_roll_no: int = Field(..., title="Student Roll No", description="Enter Student Roll No")

class PiaicCardInputSchema(BaseTool):  
    name: str = "Piaic student card generator"
    description: str = "this function will create Piaic student card"
    args_schema: Type[BaseModel] = CardInputSchema  
    
    def _run(self, student_name: str, student_roll_no: int ) -> str:
        # Your tool's logic here
        return f""" PIAIC student card
                    student name: {student_name}
                    student roll no: {student_roll_no}
                    student class: Agentic AI
                    Pakistan zindabd!
        """
     
@tool("PIAIC fee update")
def my_tool(roll_no: int) -> dict | str:
    """this function search piaic student fee updates, it will required roll no of PIAIC student"""
    #database

    data = {100:'paid',
         200:'unpaid'}


    status = data.get(roll_no)

    if status:
      return {"status": status}
    else:
      return "student not found"


    