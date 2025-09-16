from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from .filters import FilterOptions

class SearchQuery(BaseModel):
    type: str
    query: Dict[str, Any]
    filters: Optional[FilterOptions] = None
    origin: Optional[str]
    destination: str
    dateFrom: str
    dateTo: Optional[str]
    passengers: int
    budgetMin: Optional[float]
    budgetMax: Optional[float]

class Location(BaseModel):
    city: str
    address: str
    coordinates: dict

class Hotel(BaseModel):
    id: str
    name: str
    location: Location
    rating: float
    price_per_night: float
    amenities: List[str]
    images: List[str]
    availability: bool

class SearchResponse(BaseModel):
    hotels: List[Hotel]
    total: int
