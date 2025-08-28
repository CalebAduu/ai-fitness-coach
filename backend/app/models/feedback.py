from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class FeedbackAnalysis(BaseModel):
    sentiment: str
    key_issues: List[str]
    suggestions: List[str]
    adaptation_reason: str
    confidence_score: float

class FeedbackSummary(BaseModel):
    total_feedback: int
    positive_count: int
    negative_count: int
    neutral_count: int
    common_issues: List[str]
    improvement_areas: List[str]
