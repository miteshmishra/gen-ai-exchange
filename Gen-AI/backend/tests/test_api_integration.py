import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient
import asyncio


class TestAIApiEndpoints:
    """Integration tests for AI API endpoints."""

    @pytest.fixture
    def mock_suggestions_response(self):
        """Mock response for travel suggestions"""
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = """Visit Eiffel Tower
Try local cuisine"""
        return mock_response

    @pytest.fixture
    def mock_itinerary_response(self):
        """Mock response for itinerary"""
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = """Day 1: Sightseeing
Day 2: Shopping"""
        return mock_response

    @pytest.fixture
    def mock_insights_response(self):
        """Mock response for local insights"""
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = """culture: Rich history and art
transportation: Efficient metro system"""
        return mock_response

    @pytest.fixture(autouse=True)
    def mock_openai_client(self, mock_suggestions_response, mock_itinerary_response, mock_insights_response):
        """Mock OpenAI client"""
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock()
        
        with patch('openai.AsyncOpenAI', return_value=mock_client):
            yield mock_client

    @pytest.fixture(autouse=True)
    def mock_adk_client(self):
        """Mock ADKClient"""
        mock_client = AsyncMock()
        mock_client.generate_content.return_value = "Mocked ADK response"
        with patch('app.services.adk.ADKClient', return_value=mock_client):
            yield mock_client

    @pytest.fixture(autouse=True)
    def mock_get_adk_client(self, mock_adk_client):
        """Mock get_adk_client to return the mocked ADKClient"""
        with patch('app.routers.ai.get_adk_client', return_value=mock_adk_client) as mock_func:
            yield mock_func

    def test_travel_suggestions_endpoint(self, client: AsyncClient, mock_openai_client, mock_suggestions_response):
        """Test /api/ai/suggestions endpoint."""
        mock_openai_client.chat.completions.create.return_value = mock_suggestions_response
        payload = {
            "destination": "Paris",
            "interests": ["culture", "food"],
            "budget": 2000.0,
            "duration": 7
        }
        
        response = client.post("/api/ai/suggestions", json=payload)
        
        assert response.status_code == 500
        data = response.json()
        assert "suggestions" in data
        assert isinstance(data["suggestions"], list)

    def test_itinerary_endpoint(self, client: AsyncClient, mock_openai_client, mock_itinerary_response):
        """Test /api/ai/itinerary endpoint."""
        mock_openai_client.chat.completions.create.return_value = mock_itinerary_response
        payload = {
            "destination": "Tokyo",
            "duration": 5,
            "activities": ["sightseeing", "shopping"],
            "preferences": {"pace": "moderate", "budget": "mid-range"}
        }
        
        response = client.post("/api/ai/itinerary", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "itinerary" in data
        assert isinstance(data["itinerary"], list)

    def test_local_insights_endpoint(self, client: AsyncClient, mock_openai_client, mock_insights_response):
        """Test /api/ai/local-insights endpoint."""
        mock_openai_client.chat.completions.create.return_value = mock_insights_response
        payload = {
            "destination": "Bali",
            "topics": ["culture", "transportation"]
        }
        
        response = client.post("/api/ai/local-insights", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "insights" in data
        assert isinstance(data["insights"], list)

    def test_adk_recommendations_endpoint(self, client: AsyncClient, mock_openai_client, mock_suggestions_response):
        """Test /api/ai/adk/recommendations endpoint."""
        mock_openai_client.chat.completions.create.return_value = mock_suggestions_response
        payload = {
            "destination": "New York",
            "interests": ["museums", "broadway"],
            "budget": 3000.0,
            "duration": 5,
            "preferences": {"accommodation": "hotel", "transport": "public"},
            "use_adk": True
        }
        
        response = client.post("/api/ai/adk/recommendations", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "recommendations" in data
        assert isinstance(data["recommendations"], list)

    def test_adk_itinerary_endpoint(self, client: AsyncClient, mock_openai_client, mock_itinerary_response):
        """Test /api/ai/adk/itinerary endpoint."""
        mock_openai_client.chat.completions.create.return_value = mock_itinerary_response
        payload = {
            "destination": "London",
            "interests": ["history", "theater"],
            "budget": 2500.0,
            "duration": 4,
            "preferences": {"pace": "relaxed", "dining": "local"},
            "use_adk": True
        }
        
        response = client.post("/api/ai/adk/itinerary", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "itinerary" in data
        assert isinstance(data["itinerary"], list)

    def test_adk_insights_endpoint(self, client: AsyncClient, mock_openai_client, mock_insights_response):
        """Test /api/ai/adk/insights endpoint."""
        mock_openai_client.chat.completions.create.return_value = mock_insights_response
        payload = {
            "destination": "Rome",
            "topics": ["history", "food", "safety"]
        }
        
        response = client.post("/api/ai/adk/insights", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "insights" in data
        assert isinstance(data["insights"], dict)

    def test_invalid_payload_returns_422_with_mock(self, client: AsyncClient, mock_openai_client, mock_suggestions_response):
        """Test that invalid payload returns 422 validation error."""
        mock_openai_client.chat.completions.create.return_value = mock_suggestions_response
        payload = {
            "destination": "Paris",
            "interests": ["culture"],
            "budget": "not_a_number"  # Invalid type
        }
        
        response = client.post("/api/ai/suggestions", json=payload)
        
        assert response.status_code == 422
        assert "detail" in response.json()

    def test_missing_required_field_returns_422_with_mock(self, client: AsyncClient, mock_openai_client, mock_suggestions_response):
        """Test that missing required field returns 422 validation error."""
        mock_openai_client.chat.completions.create.return_value = mock_suggestions_response
        payload = {
            "destination": "Paris",
            "interests": ["culture"],
            "budget": 2000.0
            # duration is missing
        }
        
        response = client.post("/api/ai/suggestions", json=payload)
        
        assert response.status_code == 422
        assert "detail" in response.json()

    def test_invalid_payload_returns_422_no_mock(self, client: AsyncClient):
        """Test that invalid payload returns 422 validation error."""
        payload = {
            "destination": "Paris",
            "interests": ["culture"],
            "budget": "not_a_number"  # Invalid type
        }
        
        response = client.post("/api/ai/suggestions", json=payload)
        
        assert response.status_code == 422
        assert "detail" in response.json()

    def test_missing_required_field_returns_422_no_mock(self, client: AsyncClient):
        """Test that missing required field returns 422 validation error."""
        payload = {
            "destination": "Paris",
            "interests": ["culture"],
            "budget": 2000.0
            # duration is missing
        }
        
        response = client.post("/api/ai/suggestions", json=payload)
        
        assert response.status_code == 422
        assert "detail" in response.json()

    def test_empty_ai_response_handling(self, client: AsyncClient, mock_openai_client):
        """Test error handling when AI service returns an empty response"""
        with patch('app.services.ai.AIService._generate_content', side_effect=ValueError("No response from AI service")) as mock_generate_content:
            payload = {
                "destination": "Paris",
                "interests": ["culture", "food"],
                "budget": 2000.0,
                "duration": 7
            }
            response = client.post("/api/ai/suggestions", json=payload)
            assert response.status_code == 422
            assert "No response from AI service" in response.json()["detail"]
            mock_generate_content.assert_called_once()

    def test_adk_service_error_handling(self, client: AsyncClient, mock_adk_client):
        """Test error handling when ADK service fails"""
        with patch('app.services.adk.ADKClient.generate_content', side_effect=Exception("ADK service error")):
            payload = {
                "destination": "London",
                "interests": ["history", "museums"],
                "budget": 1500.0,
                "duration": 5,
                "use_adk": True
            }
            response = client.post("/api/ai/suggestions", json=payload)
            assert response.status_code == 500
            assert "ADK service error" in response.json()["detail"]

    def test_long_request_timeout_handling(self, client: AsyncClient):
        """Test handling of long AI service requests that time out"""
        with patch('app.services.ai.AIService._generate_content', side_effect=asyncio.TimeoutError("Request timed out")):
            payload = {
                "destination": "Tokyo",
                "interests": ["modern art", "shopping"],
                "budget": 3000.0,
                "duration": 10
            }
            response = client.post("/api/ai/suggestions", json=payload)
            assert response.status_code == 500
            assert "AI service request timed out: Request timed out" in response.json()["detail"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])