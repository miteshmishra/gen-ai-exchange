from fastapi import APIRouter, Depends, HTTPException
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from ..models.analytics import UserAnalytics, SearchAnalytics
from ..services.analytics import AnalyticsService
from ..core.security import get_current_user
from ..db.session import get_db
from ..models.database import User as DBUser

router = APIRouter()

@router.get(
    "/user/{user_id}",
    response_model=UserAnalytics,
    responses={
        200: {
            "description": "User analytics data retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "user_id": 1,
                        "total_searches": 25,
                        "favorite_destinations": ["Paris", "Tokyo", "New York"],
                        "search_patterns": {
                            "most_searched_city": "Paris",
                            "average_budget": 1500,
                            "preferred_amenities": ["WiFi", "Pool", "Breakfast"]
                        },
                        "last_activity": "2024-03-16T10:30:00Z"
                    }
                }
            }
        },
        403: {
            "description": "Not authorized to access this user's analytics",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authorized to access this user's analytics"}
                }
            }
        },
        401: {
            "description": "Not authenticated",
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            }
        }
    }
)
async def get_user_analytics(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get analytics data for a specific user.
    
    Parameters:
    - **user_id**: ID of the user to get analytics for
    
    Returns detailed analytics about the user's activity, including:
    - Total number of searches
    - Favorite destinations
    - Search patterns and preferences
    - Last activity timestamp
    
    Note: Users can only access their own analytics data.
    """
    # Check if the user has permission to access this data
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user's analytics"
        )
    
    return await AnalyticsService.get_user_analytics(user_id, db)

@router.get(
    "/search",
    response_model=SearchAnalytics,
    responses={
        200: {
            "description": "Search analytics data retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "total_searches": 1000,
                        "popular_destinations": [
                            {"city": "Paris", "count": 150},
                            {"city": "London", "count": 120},
                            {"city": "Tokyo", "count": 100}
                        ],
                        "average_budget": 1200,
                        "common_amenities": [
                            {"amenity": "WiFi", "frequency": 0.95},
                            {"amenity": "Breakfast", "frequency": 0.8},
                            {"amenity": "Pool", "frequency": 0.6}
                        ],
                        "peak_search_times": {
                            "day_of_week": "Sunday",
                            "hour_of_day": 20
                        }
                    }
                }
            }
        },
        401: {
            "description": "Not authenticated",
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials"}
                }
            }
        }
    }
)
async def get_search_analytics(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get overall search analytics data across all users.
    
    Returns aggregated analytics including:
    - Total number of searches performed
    - Popular destinations and their search frequencies
    - Average budget across all searches
    - Most commonly requested amenities
    - Peak search times and patterns
    
    Note: Requires authentication but available to all authenticated users.
    """
    return await AnalyticsService.get_search_analytics(db)
