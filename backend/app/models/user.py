from pydantic import BaseModel
from typing import List, Optional

class UserProfileResponse(BaseModel):
    id: str
    age: int
    sex: str
    weight_kg: float
    height_cm: float
    fitness_level: str
    goals: List[str]
    medical_conditions: List[str]
    allergies: List[str]
    days_per_week: int
    injuries: List[str]
    equipment: List[str]

class UserProfileRequest(BaseModel):
    name: str
    age: int
    sex: str
    weight_kg: float
    height_cm: float
    fitness_level: str
    goals: List[str]
    medical_conditions: List[str] = []
    allergies: List[str] = []
    days_per_week: int
    injuries: List[str] = []
    equipment: List[str] = []
