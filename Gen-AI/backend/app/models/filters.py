from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import date

class PriceRange(BaseModel):
    min: float
    max: float

class TripDuration(BaseModel):
    min: int
    max: int

class TravelDates(BaseModel):
    start: str
    end: str

class FilterOptions(BaseModel):
    priceRange: PriceRange
    rating: float
    amenities: List[str]
    travelDates: TravelDates
    tripDuration: TripDuration
