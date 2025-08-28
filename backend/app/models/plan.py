from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class WorkoutPlan(BaseModel):
    week: str
    days: List[Dict[str, Any]]
    summary: str
    total_duration_minutes: int
    difficulty_level: str

class MealPlan(BaseModel):
    week: str
    days: List[Dict[str, Any]]
    summary: str
    total_calories: int
    macronutrients: Dict[str, float]

class PlanGenerationRequest(BaseModel):
    user_profile: Dict[str, Any]
    week: str
    plan_type: str  # "workout" or "meal"

class PlanAdaptationRequest(BaseModel):
    user_profile: Dict[str, Any]
    current_plan: Dict[str, Any]
    feedback: str
    adaptation_reason: str
