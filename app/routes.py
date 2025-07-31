from fastapi import APIRouter
from pydantic import BaseModel
from app.rag_chain import chat_response
#from app.rag_cohere import chat_response

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/api/chat")
def ask_question(query: QueryRequest):
    answer = chat_response(query.question)
    return {"answer": answer}

