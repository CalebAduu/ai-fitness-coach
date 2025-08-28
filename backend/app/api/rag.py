from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

from app.services.ai_service import AIService

router = APIRouter(prefix="/rag", tags=["RAG Knowledge Base"])

class DocumentRequest(BaseModel):
    content: str
    source: str
    doc_type: str = "md"

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class ContextRequest(BaseModel):
    query: str
    max_length: int = 2000

@router.get("/stats")
async def get_rag_statistics():
    """Get RAG knowledge base statistics"""
    try:
        ai_service = AIService()
        stats = ai_service.get_rag_statistics()
        return {
            "success": True,
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

@router.post("/search")
async def search_rag_knowledge(request: SearchRequest):
    """Search the RAG knowledge base"""
    try:
        ai_service = AIService()
        results = ai_service.search_rag_knowledge(request.query, request.top_k)
        return {
            "success": True,
            "query": request.query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search: {str(e)}")

@router.post("/context")
async def get_rag_context(request: ContextRequest):
    """Get context from RAG knowledge base"""
    try:
        ai_service = AIService()
        context = ai_service.get_rag_context(request.query, request.max_length)
        return {
            "success": True,
            "query": request.query,
            "context": context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get context: {str(e)}")

@router.post("/add-document")
async def add_document(request: DocumentRequest):
    """Add a new document to the RAG knowledge base"""
    try:
        ai_service = AIService()
        doc_id = ai_service.add_rag_document(
            request.content, 
            request.source, 
            request.doc_type
        )
        return {
            "success": True,
            "document_id": doc_id,
            "message": "Document added successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add document: {str(e)}")

@router.get("/health")
async def rag_health_check():
    """Health check for RAG service"""
    try:
        ai_service = AIService()
        stats = ai_service.get_rag_statistics()
        return {
            "status": "healthy",
            "documents_loaded": stats["total_documents"],
            "sources_available": len(stats["sources"])
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
