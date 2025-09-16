from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from ..models.database import SearchHistory, User, Favorite
from collections import Counter

class AnalyticsService:
    @staticmethod
    async def get_user_analytics(user_id: int, db: Session) -> Dict[str, Any]:
        """Get analytics data for a specific user."""
        # Get user's search history
        searches = (
            db.query(SearchHistory)
            .filter(SearchHistory.user_id == user_id)
            .order_by(SearchHistory.created_at.desc())
            .all()
        )

        # Get user's favorites
        favorites = (
            db.query(Favorite)
            .filter(Favorite.user_id == user_id)
            .order_by(Favorite.created_at.desc())
            .all()
        )

        # Calculate search patterns
        search_types = Counter(search.search_type for search in searches)
        destinations = Counter(
            search.query.get('destination') 
            for search in searches 
            if search.query.get('destination')
        )

        return {
            "total_searches": len(searches),
            "search_patterns": dict(search_types),
            "favorite_destinations": [dest for dest, _ in destinations.most_common(5)],
            "recent_searches": [
                {
                    "type": search.search_type,
                    "query": search.query,
                    "date": search.created_at.isoformat()
                }
                for search in searches[:5]
            ],
            "favorites": [
                {
                    "type": fav.item_type,
                    "data": fav.item_data,
                    "date": fav.created_at.isoformat()
                }
                for fav in favorites
            ]
        }

    @staticmethod
    async def get_search_analytics(db: Session) -> Dict[str, Any]:
        """Get overall search analytics data."""
        now = datetime.utcnow()
        day_ago = now - timedelta(days=1)
        week_ago = now - timedelta(days=7)

        # Get daily searches
        daily_searches = (
            db.query(func.count(SearchHistory.id))
            .filter(SearchHistory.created_at >= day_ago)
            .scalar()
        )

        # Get search types distribution
        search_types = (
            db.query(
                SearchHistory.search_type,
                func.count(SearchHistory.id).label('count')
            )
            .group_by(SearchHistory.search_type)
            .all()
        )

        # Get popular destinations
        searches = (
            db.query(SearchHistory)
            .filter(SearchHistory.created_at >= week_ago)
            .all()
        )
        destinations = Counter(
            search.query.get('destination')
            for search in searches
            if search.query.get('destination')
        )

        # Calculate conversion rate (users who searched and then favorited)
        total_users = db.query(func.count(User.id)).scalar()
        users_with_favorites = (
            db.query(func.count(func.distinct(Favorite.user_id)))
            .scalar()
        )
        conversion_rate = (users_with_favorites / total_users * 100) if total_users > 0 else 0

        return {
            "daily_searches": daily_searches,
            "search_types": dict(search_types),
            "popular_destinations": [
                {"destination": dest, "count": count}
                for dest, count in destinations.most_common(10)
            ],
            "conversion_rate": round(conversion_rate, 2),
            "total_users": total_users,
            "total_searches": len(searches)
        }
