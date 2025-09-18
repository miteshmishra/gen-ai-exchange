from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from ..services.ai import AIService
from ..services.adk import get_adk_client
from ..models.ai import TravelSuggestionRequest, ItineraryRequest, LocalInsightsRequest, ADKTravelRequest
from ..core.security import get_current_user

router = APIRouter()

def get_ai_service() -> AIService:
    return AIService(adk_client_instance=get_adk_client())

@router.post(
    "/suggestions",
    response_model=Dict[str, Any],
    responses={
        200: {
            "description": "Successfully generated travel suggestions",
            "content": {
                "application/json": {
                    "example": {
                        "suggestions": [
                            "Visit the iconic Eiffel Tower and enjoy panoramic views of Paris",
                            "Take a romantic Seine River cruise at sunset",
                            "Explore world-class art at the Louvre Museum",
                            "Experience French cuisine at local bistros in Le Marais",
                            "Stroll through the charming Montmartre neighborhood"
                        ],
                        "destination": "Paris",
                        "success": True
                    }
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid request parameters"}
                }
            }
        },
        500: {
            "description": "AI Service Error",
            "content": {
                "application/json": {
                    "example": {"error": "Failed to generate travel suggestions"}
                }
            }
        },
        504: {
            "description": "Gateway Timeout",
            "content": {
                "application/json": {
                    "example": {"error": "Request timed out"}
                }
            }
        }
    }
)
async def get_travel_suggestions(request: TravelSuggestionRequest, ai_service: AIService = Depends(get_ai_service)) -> Dict[str, Any]:
    """
    Get AI-powered travel suggestions based on user preferences.
    
    Example Request:
    ```json
    {
        "destination": "Paris",
        "interests": ["art", "food", "culture", "history"],
        "budget": 2000.0,
        "duration": 5,
        "use_adk": true
    }
    ```
    """
    try:
        suggestions = await ai_service.get_travel_suggestions(
            destination=request.destination,
            interests=request.interests,
            budget=request.budget,
            duration=request.duration,
            use_adk=request.use_adk
        )
        return suggestions
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/itinerary",
    response_model=Dict[str, Any],
    responses={
        200: {
            "description": "Successfully generated travel itinerary",
            "content": {
                "application/json": {
                    "example": {
                        "itinerary": {
                            "day_1": [
                                {
                                    "time": "09:00",
                                    "activity": "Visit Eiffel Tower",
                                    "duration": "2 hours",
                                    "notes": "Book tickets in advance to avoid queues"
                                },
                                {
                                    "time": "12:00",
                                    "activity": "Lunch at Le Marais",
                                    "duration": "1.5 hours",
                                    "notes": "Try local French cuisine"
                                }
                            ],
                            "day_2": [
                                {
                                    "time": "10:00",
                                    "activity": "Louvre Museum Tour",
                                    "duration": "3 hours",
                                    "notes": "Focus on main attractions like Mona Lisa"
                                }
                            ]
                        },
                        "destination": "Paris",
                        "success": True
                    }
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid request parameters"}
                }
            }
        }
    }
)
async def generate_itinerary(request: ItineraryRequest, ai_service: AIService = Depends(get_ai_service)) -> Dict[str, Any]:
    """
    Generate a personalized travel itinerary using AI.
    
    Example Request:
    ```json
    {
        "destination": "Paris",
        "duration": 2,
        "activities": ["sightseeing", "museums", "dining"],
        "preferences": {
            "pace": "moderate",
            "meal_times": {
                "breakfast": "09:00",
                "lunch": "12:00",
                "dinner": "19:00"
            },
            "interests": ["art", "history", "food"]
        },
        "use_adk": true
    }
    ```
    """
    try:
        itinerary = await ai_service.generate_itinerary(
            destination=request.destination,
            duration=request.duration,
            activities=request.activities,
            preferences=request.preferences,
            use_adk=request.use_adk
        )
        return itinerary
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/local-insights",
    response_model=Dict[str, Any],
    responses={
        200: {
            "description": "Successfully generated local insights",
            "content": {
                "application/json": {
                    "example": {
                        "insights": {
                            "culture": "Rich history...",
                            "transportation": "Various options..."
                        }
                    }
                }
            },
        },
        400: {"description": "Invalid request parameters"},
        500: {"description": "Internal server error"},
    },
)
async def get_local_insights(request: LocalInsightsRequest, ai_service: AIService = Depends(get_ai_service)) -> Dict[str, Any]:
    """
    Generates local insights for a given destination and topics.
    """
    try:
        insights = await ai_service.get_local_insights(
            destination=request.destination,
            topics=request.topics,
            use_adk=request.use_adk
        )
        return insights
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=f"AI service timed out: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.post(
    "/adk/recommendations",
    response_model=Dict[str, Any],
    responses={
        200: {
            "description": "Successfully generated ADK travel recommendations",
            "content": {
                "application/json": {
                    "example": {
                        "recommendations": {
                            "attractions": [
                                {
                                    "name": "Eiffel Tower",
                                    "category": "Landmarks",
                                    "rating": 4.8,
                                    "description": "Iconic symbol of Paris with stunning city views",
                                    "visit_duration": "2-3 hours",
                                    "best_time": "Early morning or sunset",
                                    "tips": "Book skip-the-line tickets in advance"
                                },
                                {
                                    "name": "Le Marais Food Tour",
                                    "category": "Food & Culture",
                                    "rating": 4.9,
                                    "description": "Explore local cuisine and historic neighborhood",
                                    "visit_duration": "3 hours",
                                    "best_time": "Lunch time",
                                    "tips": "Come hungry, wear comfortable shoes"
                                }
                            ],
                            "restaurants": [
                                {
                                    "name": "L'Ami Louis",
                                    "cuisine": "French",
                                    "price_range": "€€€",
                                    "signature_dish": "Roast Chicken",
                                    "reservation_recommended": True
                                }
                            ],
                            "accommodations": [
                                {
                                    "name": "Le Petit Paris",
                                    "type": "Boutique Hotel",
                                    "location": "Latin Quarter",
                                    "price_range": "€€€",
                                    "highlights": ["Central location", "Rooftop terrace"]
                                }
                            ]
                        },
                        "destination": "Paris",
                        "success": True
                    }
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid request parameters"}
                }
            }
        }
    }
)
async def get_adk_recommendations(request: ADKTravelRequest) -> Dict[str, Any]:
    """
    Get travel recommendations using Google ADK agents.
    
    Example Request:
    ```json
    {
        "destination": "Paris",
        "interests": ["art", "food", "culture"],
        "budget": 3000.0,
        "duration": 5,
        "preferences": {
            "accommodation_type": "boutique",
            "dining_preferences": ["local", "fine_dining"],
            "accessibility_needs": [],
            "transportation": "public"
        },
        "use_adk": True
    }
    ```
    """
    recommendations = await ADKService.get_travel_recommendations(
        destination=request.destination,
        interests=request.interests,
        budget=request.budget,
        duration=request.duration,
        preferences=request.preferences
    )
    return recommendations


@router.post(
    "/adk/itinerary",
    response_model=Dict[str, Any],
    responses={
        200: {
            "description": "Successfully generated ADK smart itinerary",
            "content": {
                "application/json": {
                    "example": {
                        "itinerary": {
                            "overview": {
                                "destination": "Paris",
                                "duration": "5 days",
                                "highlights": ["Art & Museums", "Food & Wine", "Historic Sites"]
                            },
                            "daily_plans": [
                                {
                                    "day": 1,
                                    "theme": "Historic Paris",
                                    "activities": [
                                        {
                                            "time": "09:00",
                                            "activity": "Notre-Dame Cathedral",
                                            "duration": "1.5 hours",
                                            "details": {
                                                "description": "Gothic masterpiece",
                                                "location": "Île de la Cité",
                                                "tips": "View restoration progress",
                                                "transport": "Metro: Line 4"
                                            }
                                        },
                                        {
                                            "time": "11:00",
                                            "activity": "Sainte-Chapelle",
                                            "duration": "1 hour",
                                            "details": {
                                                "description": "Medieval chapel with stunning stained glass",
                                                "location": "Near Notre-Dame",
                                                "tips": "Buy combined ticket with Conciergerie",
                                                "transport": "Walking distance"
                                            }
                                        }
                                    ],
                                    "dining_suggestions": {
                                        "lunch": {
                                            "name": "Bistrot des Vosges",
                                            "time": "13:00",
                                            "cuisine": "Traditional French"
                                        },
                                        "dinner": {
                                            "name": "L'Arpège",
                                            "time": "19:30",
                                            "cuisine": "Michelin-starred French"
                                        }
                                    }
                                }
                            ],
                            "weather_forecast": {
                                "day_1": {
                                    "condition": "Sunny",
                                    "temperature": "22°C",
                                    "precipitation_chance": "10%"
                                }
                            }
                        },
                        "success": True
                    }
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid request parameters"}
                }
            }
        }
    }
)
async def generate_adk_itinerary(request: ADKTravelRequest) -> Dict[str, Any]:
    """
    Generate a smart itinerary using Google ADK agents.
    
    Example Request:
    ```json
    {
        "destination": "Paris",
        "interests": ["history", "architecture", "fine_dining"],
        "budget": 4000.0,
        "duration": 5,
        "preferences": {
            "pace": "moderate",
            "meal_preferences": {
                "dietary_restrictions": ["vegetarian"],
                "cuisine_types": ["french", "fusion"]
            },
            "activity_types": ["guided_tours", "self_guided"],
            "transportation": "mixed"
        },
        "use_adk": True
    }
    ```
    """
    itinerary = await ADKService.generate_smart_itinerary(
        destination=request.destination,
        interests=request.interests,
        budget=request.budget,
        duration=request.duration,
        preferences=request.preferences
    )
    return itinerary


@router.post(
    "/adk/insights",
    response_model=Dict[str, Any],
    responses={
        200: {
            "description": "Successfully generated ADK local insights",
            "content": {
                "application/json": {
                    "example": {
                        "insights": {
                            "local_life": {
                                "daily_rhythm": "Parisians typically start their day around 8am, with shops opening at 10am",
                                "social_customs": "Always greet with 'Bonjour' before starting any interaction",
                                "neighborhood_vibes": {
                                    "Le Marais": "Trendy, artistic area with great shopping",
                                    "Latin Quarter": "Student-friendly, intellectual atmosphere",
                                    "Montmartre": "Bohemian, artistic with village feel"
                                }
                            },
                            "practical_tips": {
                                "transportation": {
                                    "metro": "Most efficient way to travel",
                                    "bus": "Great for scenic routes",
                                    "walking": "Best for central neighborhoods"
                                },
                                "shopping": {
                                    "markets": "Morning is best for fresh produce",
                                    "fashion": "Sales (soldes) in January and July",
                                    "souvenirs": "Avoid tourist traps near landmarks"
                                }
                            },
                            "cultural_insights": {
                                "etiquette": {
                                    "dining": "Lunch: 12-2pm, Dinner: 7:30-10pm",
                                    "tipping": "Service usually included, round up for good service",
                                    "dress_code": "Smart casual for restaurants"
                                },
                                "language": {
                                    "essential_phrases": [
                                        "Bonjour - Hello",
                                        "Merci - Thank you",
                                        "S'il vous plaît - Please"
                                    ]
                                }
                            },
                            "seasonal_advice": {
                                "best_time_to_visit": "Spring (April-June) or Fall (September-November)",
                                "events_calendar": {
                                    "spring": "Art fairs and garden shows",
                                    "summer": "Outdoor concerts and festivals",
                                    "fall": "Food and wine events",
                                    "winter": "Christmas markets and exhibitions"
                                }
                            }
                        },
                        "destination": "Paris",
                        "success": True
                    }
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid request parameters"}
                }
            }
        }
    }
)
async def get_adk_insights(request: LocalInsightsRequest) -> Dict[str, Any]:
    """
    Get comprehensive local insights using Google ADK agents.
    
    Example Request:
    ```json
    {
        "destination": "Paris",
        "topics": [
            "local_life",
            "practical_tips",
            "cultural_insights",
            "seasonal_advice"
        ]
    }
    ```
    """
    insights = await ADKService.get_comprehensive_insights(
        destination=request.destination,
        topics=request.topics
    )
    return insights
