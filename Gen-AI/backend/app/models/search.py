from pydantic import BaseModel
from typing import Optional, List

class Location(BaseModel):
    city: str
    address: Optional[str] = None
    coordinates: Optional[dict] = None

class Hotel(BaseModel):
    id: str
    name: str
    location: Location
    rating: float
    price_per_night: int
    amenities: List[str]
    images: List[str]
    availability: bool

class SearchQuery(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    check_in_date: Optional[str] = None
    check_out_date: Optional[str] = None
    guests: Optional[int] = None
    room_type: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    amenities: Optional[List[str]] = None
    destination: Optional[str] = None
    origin: Optional[str] = None
    dateFrom: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[dict]
    total_results: int
    page: int
    page_size: int