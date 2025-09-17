import requests
import pytest

def test_api_docs_available():
    """Test that the API documentation is accessible"""
    try:
        response = requests.get("http://localhost:8000/api/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()
    except requests.ConnectionError:
        pytest.skip("API server is not running")

def test_api_health():
    """Test that the API health endpoint is working"""
    try:
        response = requests.get("http://localhost:8000/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"
    except requests.ConnectionError:
        pytest.skip("API server is not running")