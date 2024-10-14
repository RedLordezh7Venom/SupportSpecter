from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from faq_bot import generate_faq_response
from customer_service_chatbot import summarize, chatbot, sentiment_analyzer, feedback_analysis
from employee_training import response_evaluation, querie_generator

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as necessary for your use case
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FAQRequest(BaseModel):
    question: str

class ChatRequest(BaseModel):
    question: str
    language: str

class FeedbackRequest(BaseModel):
    feedback: str

class EvaluationRequest(BaseModel):
    query: str
    response: str

class QueryGenRequest(BaseModel):
    sector: str
    field: str
    experience: str

class FeedbackAnalysisRequest(BaseModel):
    text: str
    organization: str

@app.get("/")
async def home():
    return JSONResponse(content={"message": "Welcome to the home page"})

@app.post("/faq")
async def faq(request: FAQRequest):
    try:
        ans = generate_faq_response(request.question)
        return JSONResponse(content={"answer": ans})
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.post("/chatbot")
async def chat(request: ChatRequest):
    try:
        resp = chatbot(request.question, request.language)
        return JSONResponse(content={"response": resp})
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.get("/summary")
async def summ():
    try:
        summary = summarize('conversation_history.csv')
        return JSONResponse(content={"summary": summary})
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.post("/sentiment")
async def sentiment(request: FeedbackRequest):
    try:
        sent = sentiment_analyzer(request.feedback)
        return JSONResponse(content={"sentiment": sent})
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/evaluation")
async def evaluation(request: EvaluationRequest):
    try:
        evaluated = response_evaluation(request.query, request.response)
        return JSONResponse(content={"evaluated": evaluated})
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/querygen")
async def querygen(request: QueryGenRequest):
    try:
        generated = querie_generator(request.sector, request.field, request.experience)
        return JSONResponse(content={"generated_query": generated})
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/feedback")
async def feedback(request: FeedbackAnalysisRequest):
    try:
        output = feedback_analysis(request.text, request.organization)
        return JSONResponse(content={"feedback_analysis": output})
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
