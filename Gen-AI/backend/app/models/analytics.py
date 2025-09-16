from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class SearchPattern(BaseModel):
    type: str
    count: int

class RecentSearch(BaseModel):
    type: str
    query: Dict[str, Any]
    date: str

class Favorite(BaseModel):
    type: str
    data: Dict[str, Any]
    date: str

class UserAnalytics(BaseModel):
    total_searches: int
    search_patterns: Dict[str, int]
    favorite_destinations: List[str]
    recent_searches: List[RecentSearch]
    favorites: List[Favorite]

class PopularDestination(BaseModel):
    destination: str
    count: int

class SearchTypeMetrics(BaseModel):
    search_type: str
    count: int

class SearchAnalytics(BaseModel):
    daily_searches: int
    search_types: Dict[str, int]
    popular_destinations: List[PopularDestination]
    conversion_rate: float
    total_users: int
    total_searches: int
