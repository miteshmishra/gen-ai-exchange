from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class UserAnalytics(BaseModel):
    user_id: int
    total_searches: int
    search_patterns: Dict[str, int] = Field(..., alias="search_patterns")
    favorite_destinations: List[str]
    recent_searches: List[Dict[str, Any]]
    favorites: List[Dict[str, Any]]

class SearchAnalytics(BaseModel):
    daily_searches: int
    search_types: Dict[str, Any]
    popular_destinations: List[Dict[str, Any]]
    conversion_rate: float
    total_users: int
    total_searches: int