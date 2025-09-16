from fastapi import APIRouter, Depends, HTTPException
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from ..models.analytics import UserAnalytics, SearchAnalytics
from ..services.analytics import AnalyticsService
from ..core.security import get_current_user
from ..db.session import get_db
from ..models.database import User as DBUser

router = APIRouter()

@router.get("/user/{user_id}", response_model=UserAnalytics)
async def get_user_analytics(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get analytics data for a specific user."""
    # Check if the user has permission to access this data
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user's analytics"
        )
    
    return await AnalyticsService.get_user_analytics(user_id, db)

@router.get("/search", response_model=SearchAnalytics)
async def get_search_analytics(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get overall search analytics data."""
    return await AnalyticsService.get_search_analytics(db)
