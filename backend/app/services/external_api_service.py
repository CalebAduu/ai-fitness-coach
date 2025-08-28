import asyncio
import aiohttp
import requests
from typing import List, Dict, Any, Optional
from cachetools import TTLCache
from asyncio_throttle import Throttler
import logging
from datetime import datetime

from ..config import settings
from ..models.external_apis import (
    USDASearchResult, USDAFoodItem, USDANutrient,
    ExerciseSearchResult, ExerciseTarget,
    WGERSearchResult, WGERExercise
)

logger = logging.getLogger(__name__)

class ExternalAPIService:
    def __init__(self):
        self.cache = TTLCache(maxsize=1000, ttl=settings.api_cache_ttl)
        self.throttler = Throttler(rate_limit=settings.api_rate_limit, period=60)
        
        # API Base URLs
        self.usda_base_url = "https://api.nal.usda.gov/fdc/v1"
        self.exercise_db_url = "https://exercisedb.p.rapidapi.com"
        self.wger_base_url = "https://wger.de/api/v2"
        
        # Headers
        self.exercise_db_headers = {
            "X-RapidAPI-Key": settings.exercise_db_api_key,
            "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
        }
        
        self.wger_headers = {
            "Authorization": f"Token {settings.wger_api_key}",
            "Content-Type": "application/json"
        }

    async def _fetch_data(self, url: str, headers: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Generic method to fetch data from external APIs with caching and rate limiting."""
        cache_key = f"{url}:{str(params)}"
        
        # Check cache first
        if cache_key in self.cache:
            logger.info(f"Cache hit for {url}")
            return self.cache[cache_key]
        
        # Rate limiting
        await self.throttler.acquire()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Cache the result
                        self.cache[cache_key] = data
                        return data
                    else:
                        logger.error(f"API request failed: {response.status} - {url}")
                        return {}
        except Exception as e:
            logger.error(f"Error fetching data from {url}: {str(e)}")
            return {}

    async def search_usda_foods(self, query: str, page_size: int = 10, page_number: int = 1) -> USDASearchResult:
        """Search USDA food database."""
        params = {
            "api_key": settings.usda_api_key,
            "query": query,
            "pageSize": page_size,
            "pageNumber": page_number,
            "dataType": ["Foundation", "SR Legacy", "Survey (FNDDS)"]
        }
        
        url = f"{self.usda_base_url}/foods/search"
        data = await self._fetch_data(url, params=params)
        
        if not data:
            return USDASearchResult(
                total_hits=0,
                current_page=page_number,
                total_pages=0,
                page_size=page_size,
                foods=[]
            )
        
        foods = []
        for food in data.get("foods", []):
            nutrients = []
            for nutrient in food.get("foodNutrients", []):
                nutrients.append(USDANutrient(
                    id=nutrient.get("nutrientId", 0),
                    number=nutrient.get("nutrientNumber", ""),
                    name=nutrient.get("nutrientName", ""),
                    amount=nutrient.get("value", 0.0),
                    unit=nutrient.get("unitName", "")
                ))
            
            foods.append(USDAFoodItem(
                fdc_id=food.get("fdcId", 0),
                description=food.get("description", ""),
                brand_owner=food.get("brandOwner"),
                ingredients=food.get("ingredients"),
                serving_size=food.get("servingSize"),
                serving_size_unit=food.get("servingSizeUnit"),
                nutrients=nutrients
            ))
        
        return USDASearchResult(
            total_hits=data.get("totalHits", 0),
            current_page=page_number,
            total_pages=(data.get("totalHits", 0) + page_size - 1) // page_size,
            page_size=page_size,
            foods=foods
        )

    async def get_usda_food_details(self, fdc_id: int) -> Optional[USDAFoodItem]:
        """Get detailed information about a specific USDA food item."""
        params = {"api_key": settings.usda_api_key}
        url = f"{self.usda_base_url}/food/{fdc_id}"
        
        data = await self._fetch_data(url, params=params)
        
        if not data:
            return None
        
        nutrients = []
        for nutrient in data.get("foodNutrients", []):
            nutrients.append(USDANutrient(
                id=nutrient.get("nutrientId", 0),
                number=nutrient.get("nutrientNumber", ""),
                name=nutrient.get("nutrientName", ""),
                amount=nutrient.get("value", 0.0),
                unit=nutrient.get("unitName", "")
            ))
        
        return USDAFoodItem(
            fdc_id=data.get("fdcId", 0),
            description=data.get("description", ""),
            brand_owner=data.get("brandOwner"),
            ingredients=data.get("ingredients"),
            serving_size=data.get("servingSize"),
            serving_size_unit=data.get("servingSizeUnit"),
            nutrients=nutrients
        )

    async def search_exercisedb_exercises(self, query: str, target: Optional[str] = None, equipment: Optional[str] = None) -> ExerciseSearchResult:
        """Search ExerciseDB for exercises."""
        # ExerciseDB doesn't have a search endpoint, so we'll get all exercises and filter
        url = f"{self.exercise_db_url}/exercises"
        data = await self._fetch_data(url, headers=self.exercise_db_headers)
        
        if not data:
            return ExerciseSearchResult(exercises=[], total_count=0)
        
        exercises = []
        for exercise in data:
            # Filter by query (name contains query)
            if query.lower() not in exercise.get("name", "").lower():
                continue
            
            # Filter by target muscle if specified
            if target and target.lower() not in exercise.get("target", "").lower():
                continue
            
            # Filter by equipment if specified
            if equipment and equipment.lower() not in exercise.get("equipment", "").lower():
                continue
            
            exercises.append(ExerciseTarget(
                bodyPart=exercise.get("bodyPart", ""),
                equipment=exercise.get("equipment", ""),
                gifUrl=exercise.get("gifUrl", ""),
                id=exercise.get("id", ""),
                name=exercise.get("name", ""),
                target=exercise.get("target", "")
            ))
        
        return ExerciseSearchResult(exercises=exercises, total_count=len(exercises))

    async def search_wger_exercises(self, query: str, category: Optional[int] = None, muscle: Optional[int] = None) -> WGERSearchResult:
        """Search WGER exercise database."""
        params = {
            "search": query,
            "limit": 20
        }
        
        if category:
            params["category"] = category
        if muscle:
            params["muscles"] = muscle
        
        url = f"{self.wger_base_url}/exercise/"
        data = await self._fetch_data(url, headers=self.wger_headers, params=params)
        
        if not data:
            return WGERSearchResult(
                count=0,
                next=None,
                previous=None,
                results=[]
            )
        
        exercises = []
        for exercise in data.get("results", []):
            exercises.append(WGERExercise(
                id=exercise.get("id", 0),
                uuid=exercise.get("uuid", ""),
                name=exercise.get("name", ""),
                description=exercise.get("description", ""),
                category=exercise.get("category", {}),
                muscles=exercise.get("muscles", []),
                muscles_secondary=exercise.get("muscles_secondary", []),
                equipment=exercise.get("equipment", []),
                variations=exercise.get("variations"),
                images=exercise.get("images", []),
                comments=exercise.get("comments", [])
            ))
        
        return WGERSearchResult(
            count=data.get("count", 0),
            next=data.get("next"),
            previous=data.get("previous"),
            results=exercises
        )

    async def get_wger_categories(self) -> List[Dict[str, Any]]:
        """Get WGER exercise categories."""
        url = f"{self.wger_base_url}/exercisecategory/"
        data = await self._fetch_data(url, headers=self.wger_headers)
        return data.get("results", [])

    async def get_wger_muscles(self) -> List[Dict[str, Any]]:
        """Get WGER muscle groups."""
        url = f"{self.wger_base_url}/muscle/"
        data = await self._fetch_data(url, headers=self.wger_headers)
        return data.get("results", [])

# Singleton instance
external_api_service = ExternalAPIService()
