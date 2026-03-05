from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# السماح للواجهة بالاتصال بالخادم
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
