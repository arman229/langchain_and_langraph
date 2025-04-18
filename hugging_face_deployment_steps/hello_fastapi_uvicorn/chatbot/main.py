from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Worldc"}

@app.get("/new")
def read_root():
    return {"Hello": "New World"}