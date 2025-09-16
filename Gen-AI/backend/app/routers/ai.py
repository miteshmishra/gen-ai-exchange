from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from ..services.ai import AIService
from ..models.ai import TravelSuggestionRequest, ItineraryRequest, LocalInsightsRequest
from ..core.security import get_current_user

router = APIRouter()

@router.post("/suggestions")
async def get_travel_suggestions(request: TravelSuggestionRequest) -> Dict[str, Any]:
    """Get AI-powered travel suggestions based on user preferences."""
    suggestions = await AIService.get_travel_suggestions(
        destination=request.destination,
        interests=request.interests,
        budget=request.budget,
        duration=request.duration
    )
    return suggestions

@router.post("/itinerary")
async def generate_itinerary(request: ItineraryRequest) -> Dict[str, Any]:
    """Generate a personalized travel itinerary using AI."""
    itinerary = await AIService.generate_itinerary(
        destination=request.destination,
        duration=request.duration,
        activities=request.activities,
        preferences=request.preferences
    )
    return itinerary

@router.post("/local-insights")
async def get_local_insights(request: LocalInsightsRequest) -> Dict[str, Any]:
    """Get AI-generated local insights about a destination."""
    insights = await AIService.get_local_insights(
        destination=request.destination,
        topics=request.topics
    )
    return insights
