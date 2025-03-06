import os
import time
import aiohttp
import chainlit as cl 
from litellm import completion
 
async def generate_response(messages):
    resp = completion(
    # model="ollama/deepseek-r1:1.5b",
    model="ollama/deepseek-coder",
    base_url="http://localhost:11434",
    messages=[{"role": "user", "content": messages}],
    temperature=0,  # Set low temperature for consistency
    system_prompt=""  # Avoid hidden instructions
)

    print(resp.choices[0].message.content )
    return  resp.choices[0].message.content 
            
            # if response.status == 200:
            #     data = await response.json()
            #     return data.get("response", "No response received.")
            # else:
            #     return f"Error {response.status}: {await response.text()}"

@cl.on_message
async def on_message(msg: cl.Message):
    start = time.time()

    # Get response from Ollama
    response_text = await generate_response(msg.content)

    # Send the final answer
    final_answer = cl.Message(content=response_text)
    await final_answer.send()
