from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from faq_bot import generate_faq_response
from customer_service_chatbot import summarize, chatbot, sentiment_analyzer

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define models for request bodies if needed (optional)
class Feedback(BaseModel):
    feedback: str

class ChatRequest(BaseModel):
    question: str
    language: str

# Home route
@app.get("/")
def home():
    return {"message": "Welcome to the home page"}

# FAQ route
@app.post("/faq")
def faq(question: str = Form(...)):
    try:
        # Generate answer
        ans = generate_faq_response(question)
        return {"answer": ans}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

# Chatbot route
@app.post("/chatbot")
def chat(request: ChatRequest):
    try:
        resp = chatbot(request.question, request.language)
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

# Summary route
@app.post("/summary")
def summ():
    try:
        summary = summarize('conversation_history.csv')
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

# Sentiment route
@app.post("/sentiment")
def sentiment(feedback: Feedback):
    try:
        sent = sentiment_analyzer(feedback.feedback)
        return {"sentiment": sent}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
