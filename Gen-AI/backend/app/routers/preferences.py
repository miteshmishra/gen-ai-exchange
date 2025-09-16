from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from ..core.security import get_current_user
from ..db.session import get_db
from ..models.database import User as DBUser
from ..models.preferences import UserPreferences
from pydantic import BaseModel
from typing import List, Optional

class PreferencesUpdate(BaseModel):
    preferred_destinations: Optional[List[str]] = None
    preferred_activities: Optional[List[str]] = None
    travel_style: Optional[str] = None
    preferred_amenities: Optional[List[str]] = None
    room_type: Optional[str] = None
    max_price_per_night: Optional[int] = None
    preferred_airlines: Optional[List[str]] = None
    seat_preference: Optional[str] = None
    cabin_class: Optional[str] = None
    email_notifications: Optional[bool] = None
    price_alerts: Optional[bool] = None
    deal_notifications: Optional[bool] = None
    preferred_currency: Optional[str] = None
    preferred_language: Optional[str] = None
    accessibility_needs: Optional[List[str]] = None

router = APIRouter()

@router.get("")
async def get_preferences(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """Get user preferences."""
    preferences = db.query(UserPreferences).filter(
        UserPreferences.user_id == current_user.id
    ).first()

    if not preferences:
        # Create default preferences
        preferences = UserPreferences(user_id=current_user.id)
        db.add(preferences)
        db.commit()
        db.refresh(preferences)

    return preferences

@router.put("")
async def update_preferences(
    preferences_update: PreferencesUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """Update user preferences."""
    preferences = db.query(UserPreferences).filter(
        UserPreferences.user_id == current_user.id
    ).first()

    if not preferences:
        preferences = UserPreferences(user_id=current_user.id)
        db.add(preferences)

    # Update only provided fields
    for field, value in preferences_update.dict(exclude_unset=True).items():
        setattr(preferences, field, value)

    db.commit()
    db.refresh(preferences)
    return preferences

@router.get("/available-options")
async def get_preference_options():
    """Get available options for preferences."""
    return {
        "travel_styles": [
            "luxury",
            "budget",
            "adventure",
            "cultural",
            "relaxation",
            "family",
            "business"
        ],
        "room_types": [
            "single",
            "double",
            "twin",
            "suite",
            "family",
            "presidential"
        ],
        "seat_preferences": [
            "window",
            "aisle",
            "no_preference"
        ],
        "cabin_classes": [
            "economy",
            "premium_economy",
            "business",
            "first"
        ],
        "currencies": [
            "USD",
            "EUR",
            "GBP",
            "JPY",
            "AUD",
            "CAD"
        ],
        "languages": [
            "en",
            "es",
            "fr",
            "de",
            "it",
            "ja"
        ],
        "amenities": [
            "wifi",
            "pool",
            "spa",
            "gym",
            "restaurant",
            "room_service",
            "parking",
            "airport_shuttle",
            "pet_friendly",
            "business_center"
        ],
        "activities": [
            "sightseeing",
            "food_and_dining",
            "shopping",
            "nature",
            "adventure_sports",
            "cultural_events",
            "nightlife",
            "relaxation",
            "family_activities"
        ],
        "accessibility_options": [
            "wheelchair_accessible",
            "elevator_access",
            "accessible_bathroom",
            "roll_in_shower",
            "hearing_accessible",
            "visual_aids",
            "service_animal_friendly"
        ]
    }
