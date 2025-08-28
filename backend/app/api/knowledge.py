from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
import time
import logging

from ..models.external_apis import (
    KnowledgeQuery, KnowledgeResponse, SearchResult,
    USDASearchResult, ExerciseSearchResult, WGERSearchResult
)
from ..services.external_api_service import external_api_service
from ..services.ai_service import ai_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/search", response_model=KnowledgeResponse)
async def search_knowledge(query: KnowledgeQuery):
    """
    Search for knowledge across multiple sources (internal RAG + external APIs).
    """
    start_time = time.time()
    
    try:
        # Use the AI service to search knowledge (which integrates internal RAG + external APIs)
        results = await ai_service.search_knowledge(query)
        
        search_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return KnowledgeResponse(
            query=query.query,
            results=results,
            total_results=len(results),
            search_time_ms=search_time,
            sources_used=query.sources or ["internal", "usda", "exercisedb", "wger"]
        )
    
    except Exception as e:
        logger.error(f"Error searching knowledge: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching knowledge: {str(e)}")

@router.get("/nutrition/search", response_model=USDASearchResult)
async def search_nutrition(
    query: str = Query(..., description="Food item to search for"),
    page_size: int = Query(10, ge=1, le=50, description="Number of results per page"),
    page_number: int = Query(1, ge=1, description="Page number")
):
    """
    Search USDA food database for nutrition information.
    """
    try:
        result = await external_api_service.search_usda_foods(
            query=query,
            page_size=page_size,
            page_number=page_number
        )
        return result
    
    except Exception as e:
        logger.error(f"Error searching USDA foods: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching nutrition database: {str(e)}")

@router.get("/nutrition/food/{fdc_id}")
async def get_food_details(fdc_id: int):
    """
    Get detailed nutrition information for a specific food item.
    """
    try:
        food = await external_api_service.get_usda_food_details(fdc_id)
        if not food:
            raise HTTPException(status_code=404, detail="Food item not found")
        return food
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting food details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting food details: {str(e)}")

@router.get("/exercises/search", response_model=ExerciseSearchResult)
async def search_exercises(
    query: str = Query(..., description="Exercise name or body part"),
    target: Optional[str] = Query(None, description="Target muscle group"),
    equipment: Optional[str] = Query(None, description="Equipment type")
):
    """
    Search ExerciseDB for exercises.
    """
    try:
        result = await external_api_service.search_exercisedb_exercises(
            query=query,
            target=target,
            equipment=equipment
        )
        return result
    
    except Exception as e:
        logger.error(f"Error searching exercises: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching exercise database: {str(e)}")

@router.get("/exercises/wger/search", response_model=WGERSearchResult)
async def search_wger_exercises(
    query: str = Query(..., description="Exercise name or description"),
    category: Optional[int] = Query(None, description="Exercise category ID"),
    muscle: Optional[int] = Query(None, description="Muscle group ID")
):
    """
    Search WGER exercise database.
    """
    try:
        result = await external_api_service.search_wger_exercises(
            query=query,
            category=category,
            muscle=muscle
        )
        return result
    
    except Exception as e:
        logger.error(f"Error searching WGER exercises: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching WGER database: {str(e)}")

@router.get("/exercises/wger/categories")
async def get_wger_categories():
    """
    Get WGER exercise categories.
    """
    try:
        categories = await external_api_service.get_wger_categories()
        return {"categories": categories}
    
    except Exception as e:
        logger.error(f"Error getting WGER categories: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting exercise categories: {str(e)}")

@router.get("/exercises/wger/muscles")
async def get_wger_muscles():
    """
    Get WGER muscle groups.
    """
    try:
        muscles = await external_api_service.get_wger_muscles()
        return {"muscles": muscles}
    
    except Exception as e:
        logger.error(f"Error getting WGER muscles: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting muscle groups: {str(e)}")

@router.get("/sources")
async def get_available_sources():
    """
    Get information about available knowledge sources.
    """
    return {
        "sources": [
            {
                "id": "internal",
                "name": "Internal Knowledge Base",
                "description": "Curated fitness and nutrition knowledge from internal documents",
                "type": "rag"
            },
            {
                "id": "usda",
                "name": "USDA Food Database",
                "description": "Comprehensive nutrition information for foods",
                "type": "api",
                "requires_key": True
            },
            {
                "id": "exercisedb",
                "name": "ExerciseDB",
                "description": "Exercise database with GIFs and instructions",
                "type": "api",
                "requires_key": True
            },
            {
                "id": "wger",
                "name": "WGER Exercise Database",
                "description": "Open-source exercise database with detailed information",
                "type": "api",
                "requires_key": True
            }
        ],
        "configuration": {
            "cache_ttl_seconds": 300,
            "rate_limit_per_minute": 10
        }
    }
