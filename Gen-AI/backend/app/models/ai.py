from pydantic import BaseModel
from typing import List, Dict, Any

class TravelSuggestionRequest(BaseModel):
    destination: str
    interests: List[str]
    budget: float
    duration: int
    use_adk: bool = False

class ItineraryRequest(BaseModel):
    destination: str
    duration: int
    activities: List[str]
    preferences: Dict[str, Any]
    use_adk: bool = False

class LocalInsightsRequest(BaseModel):
    destination: str
    topics: List[str]
    use_adk: bool = False


class ADKTravelRequest(BaseModel):
    destination: str
    interests: List[str]
    budget: float
    duration: int
    preferences: Dict[str, Any]
    use_adk: bool = True
