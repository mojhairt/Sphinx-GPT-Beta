from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Sphinx AI is running"}

@app.post("/chat")
def chat(q: Question):
    question = q.text

    # هنا سيعمل الموديل
    answer = "This is a test response: " + question

    return {"response": answer}
