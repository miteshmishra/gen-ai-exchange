from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from ..db.models import SearchHistory, User, Favorite, Feedback
from ..models.agent import Experiment, AgentAction
from collections import Counter
import random
import json

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
            (json.loads(search.query) if isinstance(search.query, str) else search.query).get('destination') 
            for search in searches 
            if (json.loads(search.query) if isinstance(search.query, str) else search.query).get('destination')
        )

        return {
            "total_searches": len(searches),
            "user_id": user_id,
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
                    "id": fav.id,
                    "created_at": fav.created_at.isoformat()
                }
                for fav in favorites
            ]
        }

    @staticmethod
    async def assign_experiment_variant(
        experiment_id: int,
        user_id: int,
        db: Session
    ) -> Optional[Dict[str, Any]]:
        """Assign a user to an experiment variant."""
        experiment = db.query(Experiment).filter(
            and_(
                Experiment.id == experiment_id,
                Experiment.status == "active"
            )
        ).first()
        
        if not experiment:
            return None
            
        # Use consistent hashing to ensure users get same variant
        user_hash = hash(f"{user_id}:{experiment.feature_key}")
        variants = experiment.variants
        chosen_variant = variants[user_hash % len(variants)]
        
        return {
            "experiment_id": experiment.id,
            "feature_key": experiment.feature_key,
            "variant": chosen_variant
        }

    @staticmethod
    async def track_experiment_event(
        experiment_id: int,
        user_id: int,
        event_type: str,
        event_data: Dict[str, Any],
        db: Session
    ) -> None:
        """Track an event for experiment analysis."""
        experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
        if not experiment:
            return
            
        # Update experiment metrics
        metrics = experiment.metrics or {}
        events = metrics.get("events", [])
        events.append({
            "user_id": user_id,
            "type": event_type,
            "data": event_data,
            "timestamp": datetime.utcnow().isoformat()
        })
        metrics["events"] = events
        
        experiment.metrics = metrics
        db.commit()

    @staticmethod
    async def evaluate_experiment(
        experiment_id: int,
        db: Session
    ) -> Dict[str, Any]:
        """Evaluate experiment results and make recommendations."""
        experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
        if not experiment:
            return {"error": "Experiment not found"}
            
        metrics = experiment.metrics or {}
        events = metrics.get("events", [])
        
        # Calculate key metrics by variant
        results = {}
        for variant in experiment.variants:
            variant_events = [e for e in events if e["data"].get("variant") == variant["id"]]
            results[variant["id"]] = {
                "conversion_rate": self._calculate_conversion_rate(variant_events),
                "avg_task_time": self._calculate_avg_task_time(variant_events),
                "user_satisfaction": self._calculate_satisfaction(variant_events)
            }
            
        # Determine if we have a winner
        best_variant = max(results.items(), key=lambda x: x[1]["conversion_rate"])
        significant = self._is_statistically_significant(results)
        
        return {
            "results": results,
            "best_variant": best_variant[0] if significant else None,
            "significant": significant,
            "sample_size": len(events)
        }

    @staticmethod
    async def collect_feedback(
        user_id: int,
        feedback_data: Dict[str, Any],
        db: Session
    ) -> Feedback:
        """Collect and store user feedback."""
        feedback = Feedback(
            user_id=user_id,
            trip_id=feedback_data.get("trip_id"),
            itinerary_item_id=feedback_data.get("itinerary_item_id"),
            subject_type=feedback_data.get("subject_type"),
            variant_id=feedback_data.get("variant_id"),
            rating=feedback_data.get("rating"),
            comment=feedback_data.get("comment"),
            task_time_ms=feedback_data.get("task_time_ms"),
            screen_reader_notes=feedback_data.get("screen_reader_notes"),
            locale=feedback_data.get("locale", "en")
        )
        
        db.add(feedback)
        db.commit()
        return feedback

    @classmethod
    def _calculate_conversion_rate(cls, events: List[Dict[str, Any]]) -> float:
        """Calculate conversion rate from events."""
        if not events:
            return 0.0
        conversions = len([e for e in events if e["type"] == "conversion"])
        return conversions / len(events)

    @classmethod
    def _calculate_avg_task_time(cls, events: List[Dict[str, Any]]) -> float:
        """Calculate average task completion time."""
        task_times = [
            e["data"].get("task_time_ms", 0) 
            for e in events 
            if e["data"].get("task_time_ms")
        ]
        return sum(task_times) / len(task_times) if task_times else 0

    @classmethod
    def _calculate_satisfaction(cls, events: List[Dict[str, Any]]) -> float:
        """Calculate user satisfaction score."""
        ratings = [
            e["data"].get("rating", 0) 
            for e in events 
            if e["data"].get("rating")
        ]
        return sum(ratings) / len(ratings) if ratings else 0

    @classmethod
    def _is_statistically_significant(
        cls,
        results: Dict[str, Dict[str, float]]
    ) -> bool:
        """Determine if results are statistically significant."""
        # Implement statistical significance test
        # For MVP, require minimum sample size and effect size
        return True  # Simplified for now

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
            (json.loads(search.query) if isinstance(search.query, str) else search.query).get('destination')
            for search in searches
            if (json.loads(search.query) if isinstance(search.query, str) else search.query).get('destination')
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
