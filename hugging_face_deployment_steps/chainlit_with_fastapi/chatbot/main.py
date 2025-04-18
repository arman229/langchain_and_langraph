from fastapi import FastAPI
from chainlit.utils import mount_chainlit
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Worldc"}

@app.get("/new")
def read_root():
    return {"Hello": "New World"} 
mount_chainlit(app=app, target="chatbot/my_cl_app.py", path="/chainlit")
