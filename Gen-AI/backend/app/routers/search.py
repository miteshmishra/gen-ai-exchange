from fastapi import APIRouter, Depends, HTTPException
from typing import Any, Dict, List, Optional
from ..models.search import SearchQuery, SearchResponse
from ..models.filters import FilterOptions
from ..services.search import SearchService
import random
import asyncio

router = APIRouter()

@router.post("/hotels", response_model=SearchResponse)
async def search_hotels(query: SearchQuery) -> Dict[str, Any]:
    """Search for hotels based on the provided criteria."""
    await asyncio.sleep(random.uniform(0.2, 0.6))
    hotels = []
    
    # Generate initial results
    for i in range(random.randint(8, 15)):
        hotel = {
            "id": f"HT{random.randint(1000, 9999)}",
            "name": f"Hotel {random.choice(['Grand', 'Royal', 'Premium', 'Plaza'])} {random.choice(['Central', 'Downtown', 'Plaza', 'Bay'])}",
            "location": {
                "city": query.query.get("destination", "New York"),
                "address": f"{random.randint(100, 999)} Main St",
                "coordinates": {
                    "lat": round(random.uniform(25, 48), 6),
                    "lng": round(random.uniform(-120, -70), 6)
                }
            },
            "rating": round(random.uniform(3.5, 5.0), 1),
            "price_per_night": random.randint(80, 400),
            "amenities": random.sample([
                "WiFi", "Pool", "Gym", "Spa", "Restaurant",
                "Bar", "Parking", "Pet Friendly", "Business Center"
            ], random.randint(3, 6)),
            "images": [f"https://picsum.photos/300/200?random={i}"],
            "availability": True
        }
        
        # Apply filters if provided
        if query.filters:
            # Price range filter
            if not (query.filters.priceRange.min <= hotel["price_per_night"] <= query.filters.priceRange.max):
                continue
                
            # Rating filter
            if hotel["rating"] < query.filters.rating:
                continue
                
            # Amenities filter
            if query.filters.amenities:
                if not all(amenity in hotel["amenities"] for amenity in query.filters.amenities):
                    continue
                    
        hotels.append(hotel)
    
    return {
        "hotels": hotels,
        "total": len(hotels)
    }

@router.post("/flights")
async def search_flights(query: SearchQuery) -> Dict[str, Any]:
    """Search for flights based on the provided criteria."""
    # Implement flight search logic
    pass

@router.post("/experiences")
async def search_experiences(query: SearchQuery) -> Dict[str, Any]:
    """Search for experiences based on the provided criteria."""
    # Implement experiences search logic
    pass
