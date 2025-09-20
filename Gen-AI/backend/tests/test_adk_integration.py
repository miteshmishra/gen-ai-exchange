import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient


class TestADKAiApiEndpoints:
    """Integration tests for AI API endpoints with ADK functionality."""

    @pytest.fixture
    def mock_adk_response(self):
        """Mock response for ADK generated content"""
        return "mocked adk response"

    @pytest.fixture(autouse=True)
    def mock_adk_client(self, mock_adk_response):
        """Mock ADKClient"""
        mock_adk_instance = MagicMock()
        mock_adk_instance.generate_content = AsyncMock(return_value=mock_adk_response)
        with patch('app.services.adk.ADKClient', return_value=mock_adk_instance):
            yield mock_adk_instance

    @pytest.fixture
    def mock_openai_response(self):
        """Mock response for OpenAI generated content"""
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message = AsyncMock()
        mock_response.choices[0].message.content = "OpenAI generated content"
        return mock_response

    @pytest.fixture(autouse=True)
    def mock_openai_client(self, mock_openai_response):
        """Mock OpenAI client"""
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_openai_response)
        with patch('openai.AsyncOpenAI', return_value=mock_client):
            yield mock_client

    @pytest.fixture
    def client(self, mock_adk_client):
        from app.main import app
        from app.routers.ai import get_ai_service
        from fastapi.testclient import TestClient
        app.dependency_overrides[get_ai_service] = lambda: get_ai_service(mock_adk_client=mock_adk_client)
        with TestClient(app) as client:
            yield client
        app.dependency_overrides = {}

    @pytest.mark.asyncio
    async def test_travel_suggestions_with_adk(self, client: AsyncClient, mock_adk_client):
        """Test /api/ai/suggestions endpoint with use_adk=True."""
        payload = {
            "destination": "Paris",
            "interests": ["culture", "food"],
            "budget": 2000.0,
            "duration": 7,
            "use_adk": True
        }
        response = client.post("/api/ai/suggestions", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "suggestions" in data
        assert data["suggestions"] == ["mocked adk response"]
        mock_adk_client.generate_content.assert_called_once()

    @pytest.mark.asyncio
    async def test_travel_suggestions_without_adk(self, client: AsyncClient, mock_openai_client):
        """Test /api/ai/suggestions endpoint with use_adk=False."""
        payload = {
            "destination": "Paris",
            "interests": ["culture", "food"],
            "budget": 2000.0,
            "duration": 7,
            "use_adk": False
        }
        response = client.post("/api/ai/suggestions", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "suggestions" in data
        assert data["suggestions"] == ["OpenAI generated content"]
        mock_openai_client.chat.completions.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_itinerary_with_adk(self, client: AsyncClient, mock_adk_client):
        """Test /api/ai/itinerary endpoint with use_adk=True."""
        payload = {
            "destination": "Tokyo",
            "duration": 5,
            "activities": ["sightseeing", "shopping"],
            "preferences": {"pace": "moderate", "budget": "mid-range"},
            "use_adk": True
        }
        response = client.post("/api/ai/itinerary", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "itinerary" in data
        assert data["itinerary"] == ["mocked adk response"]
        mock_adk_client.generate_content.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_itinerary_without_adk(self, client: AsyncClient, mock_openai_client):
        """Test /api/ai/itinerary endpoint with use_adk=False."""
        payload = {
            "destination": "Tokyo",
            "duration": 5,
            "activities": ["sightseeing", "shopping"],
            "preferences": {"pace": "moderate", "budget": "mid-range"},
            "use_adk": False
        }
        response = client.post("/api/ai/itinerary", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "itinerary" in data
        assert data["itinerary"] == ["OpenAI generated content"]
        mock_openai_client.chat.completions.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_local_insights_with_adk(self, client: AsyncClient, mock_adk_client):
        """Test /api/ai/local-insights endpoint with use_adk=True."""
        payload = {
            "destination": "Bali",
            "topics": ["culture", "transportation"],
            "use_adk": True
        }
        response = client.post("/api/ai/local-insights", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "insights" in data
        assert data["insights"] == ["mocked adk response"]
        mock_adk_client.generate_content.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_local_insights_without_adk(self, client: AsyncClient, mock_openai_client):
        """Test /api/ai/local-insights endpoint with use_adk=False."""
        payload = {
            "destination": "Bali",
            "topics": ["culture", "transportation"],
            "use_adk": False
        }
        response = client.post("/api/ai/local-insights", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "insights" in data
        assert data["insights"] == ["OpenAI generated content"]
        mock_openai_client.chat.completions.create.assert_called_once()