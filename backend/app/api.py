from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.rag.retriever import get_retriever
from app.rag.generator import get_rag_chain
import logging
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()
logger = logging.getLogger(__name__)

executor = ThreadPoolExecutor(max_workers=2)  

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]

@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    try:
        retriever = get_retriever()
        chain = get_rag_chain(retriever)        

        response = chain({
            "question": request.question
        })

        
        answer = response["result"]
        source_docs = response["source_documents"]
        
        sources = list(set([
            os.path.basename(doc.metadata.get("source", "unknown")) 
            for doc in source_docs
        ]))
        
        return AnswerResponse(answer=answer, sources=sources)
        
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Knowledge base not ready. Please run ingestion first.")
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/post")
def post():
    return {"message": "Hello World"}
