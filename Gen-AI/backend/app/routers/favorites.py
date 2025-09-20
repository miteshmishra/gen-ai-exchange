from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.models import Favorite
from ..core.security import get_current_user
from ..db.session import get_db
from datetime import datetime

router = APIRouter()

@router.post("/{item_type}/{item_id}")
async def add_favorite(
    item_type: str,
    item_id: str,
    item_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Add an item to user's favorites."""
    # Check if already favorited
    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.item_type == item_type,
        Favorite.item_id == item_id
    ).first()

    if existing_favorite:
        raise HTTPException(
            status_code=400,
            detail="Item already in favorites"
        )

    # Create new favorite
    favorite = Favorite(
        user_id=current_user.id,
        item_type=item_type,
        item_id=item_id,
        item_data=item_data
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    
    return {
        "message": "Added to favorites",
        "favorite": {
            "id": favorite.id,
            "item_type": favorite.item_type,
            "item_id": favorite.item_id,
            "created_at": favorite.created_at
        }
    }

@router.delete("/{item_type}/{item_id}")
async def remove_favorite(
    item_type: str,
    item_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Remove an item from user's favorites."""
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.item_type == item_type,
        Favorite.item_id == item_id
    ).first()

    if not favorite:
        raise HTTPException(
            status_code=404,
            detail="Item not found in favorites"
        )

    db.delete(favorite)
    db.commit()
    
    return {"message": "Removed from favorites"}

@router.get("/")
async def get_favorites(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all favorites for the current user."""
    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id
    ).all()

    return {
        "favorites": [
            {
                "id": fav.id,
                "item_type": fav.item_type,
                "item_id": fav.item_id,
                "item_data": fav.item_data,
                "created_at": fav.created_at
            }
            for fav in favorites
        ]
    }

@router.get("/{item_type}")
async def get_favorites_by_type(
    item_type: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get user's favorites filtered by type."""
    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.item_type == item_type
    ).all()

    return {
        "favorites": [
            {
                "id": fav.id,
                "item_type": fav.item_type,
                "item_id": fav.item_id,
                "item_data": fav.item_data,
                "created_at": fav.created_at
            }
            for fav in favorites
        ]
    }
