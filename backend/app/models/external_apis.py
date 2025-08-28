from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# USDA Food Database Models
class USDANutrient(BaseModel):
    id: int
    number: str
    name: str
    amount: float
    unit: str

class USDAFoodItem(BaseModel):
    fdc_id: int
    description: str
    brand_owner: Optional[str] = None
    ingredients: Optional[str] = None
    serving_size: Optional[float] = None
    serving_size_unit: Optional[str] = None
    nutrients: List[USDANutrient] = []

class USDASearchResult(BaseModel):
    total_hits: int
    current_page: int
    total_pages: int
    page_size: int
    foods: List[USDAFoodItem]

# ExerciseDB Models
class ExerciseTarget(BaseModel):
    bodyPart: str
    equipment: str
    gifUrl: str
    id: str
    name: str
    target: str

class ExerciseSearchResult(BaseModel):
    exercises: List[ExerciseTarget]
    total_count: int

# WGER Exercise Database Models
class WGERExercise(BaseModel):
    id: int
    uuid: str
    name: str
    description: str
    category: Dict[str, Any]
    muscles: List[Dict[str, Any]]
    muscles_secondary: List[Dict[str, Any]]
    equipment: List[Dict[str, Any]]
    variations: Optional[int] = None
    images: List[Dict[str, Any]] = []
    comments: List[Dict[str, Any]] = []

class WGERSearchResult(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[WGERExercise]

# Generic Knowledge Search Models
class SearchResult(BaseModel):
    source: str  # "internal", "usda", "exercisedb", "wger"
    title: str
    content: str
    metadata: Dict[str, Any] = {}
    relevance_score: Optional[float] = None

class KnowledgeQuery(BaseModel):
    query: str
    sources: Optional[List[str]] = None  # ["internal", "usda", "exercisedb", "wger"]
    max_results: int = 10
    include_metadata: bool = True

class KnowledgeResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_results: int
    search_time_ms: float
    sources_used: List[str]
