from fastapi.middleware.cors import CORSMiddleware
from app.api import knowledge, rag
from app.config import settings

app = FastAPI(
    title="AI Fitness Coach API",
    description="AI-powered fitness coaching with personalized workout and meal plans",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(knowledge.router, prefix="/api/knowledge", tags=["knowledge"])
app.include_router(rag.router, prefix="/api", tags=["RAG Knowledge Base"])

@app.get("/")
async def root():
    return {"message": "AI Fitness Coach API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": ["knowledge", "rag"]}

@app.get("/test-rag")
async def test_rag():
    """Test RAG service without requiring API keys"""
    try:
        from app.services.rag_service import RAGService
        rag_service = RAGService()
        stats = rag_service.get_statistics()
        return {
            "status": "success",
            "message": "RAG service is working!",
            "statistics": stats
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"RAG service error: {str(e)}"
        }
