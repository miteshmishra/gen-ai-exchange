import pytest
from pydantic import ValidationError

from app.models.ai import (
    TravelSuggestionRequest,
    ItineraryRequest,
    LocalInsightsRequest,
    ADKTravelRequest
)


class TestAIModels:
    """Test cases for AI request models."""

    def test_travel_suggestion_request_valid(self):
        """Test valid TravelSuggestionRequest creation."""
        data = {
            "destination": "Paris",
            "interests": ["culture", "food"],
            "budget": 2000.0,
            "duration": 7
        }
        request = TravelSuggestionRequest(**data)
        
        assert request.destination == "Paris"
        assert request.interests == ["culture", "food"]
        assert request.budget == 2000.0
        assert request.duration == 7

    def test_travel_suggestion_request_missing_field(self):
        """Test TravelSuggestionRequest with missing required field."""
        data = {
            "destination": "Paris",
            "interests": ["culture"],
            "budget": 2000.0
            # duration is missing
        }
        
        with pytest.raises(ValidationError):
            TravelSuggestionRequest(**data)

    def test_itinerary_request_valid(self):
        """Test valid ItineraryRequest creation."""
        data = {
            "destination": "Tokyo",
            "duration": 10,
            "activities": ["sightseeing", "shopping"],
            "preferences": {"pace": "moderate", "budget": "mid-range"}
        }
        request = ItineraryRequest(**data)
        
        assert request.destination == "Tokyo"
        assert request.duration == 10
        assert request.activities == ["sightseeing", "shopping"]
        assert request.preferences == {"pace": "moderate", "budget": "mid-range"}

    def test_local_insights_request_valid(self):
        """Test valid LocalInsightsRequest creation."""
        data = {
            "destination": "Bali",
            "topics": ["culture", "transportation"]
        }
        request = LocalInsightsRequest(**data)
        
        assert request.destination == "Bali"
        assert request.topics == ["culture", "transportation"]

    def test_adk_travel_request_valid(self):
        """Test valid ADKTravelRequest creation."""
        data = {
            "destination": "New York",
            "interests": ["museums", "broadway"],
            "budget": 3000.0,
            "duration": 5,
            "preferences": {"accommodation": "hotel", "transport": "public"},
            "use_adk": True
        }
        request = ADKTravelRequest(**data)
        
        assert request.destination == "New York"
        assert request.interests == ["museums", "broadway"]
        assert request.budget == 3000.0
        assert request.duration == 5
        assert request.preferences == {"accommodation": "hotel", "transport": "public"}
        assert request.use_adk == True

    def test_adk_travel_request_default_use_adk(self):
        """Test ADKTravelRequest with default use_adk value."""
        data = {
            "destination": "London",
            "interests": ["history"],
            "budget": 1500.0,
            "duration": 3,
            "preferences": {}
            # use_adk not provided, should default to True
        }
        request = ADKTravelRequest(**data)
        
        assert request.use_adk == True

    def test_adk_travel_request_invalid_budget(self):
        """Test ADKTravelRequest with invalid budget type."""
        data = {
            "destination": "Rome",
            "interests": ["architecture"],
            "budget": "not_a_number",  # Invalid type
            "duration": 4,
            "preferences": {}
        }
        
        with pytest.raises(ValidationError):
            ADKTravelRequest(**data)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])