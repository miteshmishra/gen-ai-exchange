from pydantic import BaseModel
from typing import Optional, List

class PriceRange(BaseModel):
    min: float
    max: float

class FilterOptions(BaseModel):
    priceRange: Optional[PriceRange] = None
    rating: Optional[int] = None
    amenities: Optional[List[str]] = None
    travelDates: Optional[dict] = None  # Assuming a dictionary for now, can be refined
    tripDuration: Optional[dict] = None # Assuming a dictionary for now, can be refined