import pytest
from fastapi.testclient import TestClient
from app.db.models import User
from app.routers.auth import get_password_hash

def test_search_hotels(client, test_db):
    """Test hotel search endpoint"""
    # Create a user and get authentication token
    hashed_password = get_password_hash("password123")
    user = User(email="hotel@example.com", full_name="Hotel User", hashed_password=hashed_password)
    test_db.add(user)
    test_db.commit()
    
    login_response = client.post(
        "/api/auth/login",
        data={"username": "hotel@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Test hotel search
    response = client.post(
        "/api/search/hotels",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "location": "New York",
            "checkIn": "2023-12-01",
            "checkOut": "2023-12-05",
            "guests": 2,
            "filters": {
                "priceRange": {"min": 100, "max": 500},
                "amenities": ["wifi", "pool"],
                "rating": 4
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "hotels" in data
    assert isinstance(data["hotels"], list)
    assert "total" in data

def test_search_flights(client, test_db):
    """Test flight search endpoint"""
    # Create a user and get authentication token
    hashed_password = get_password_hash("password123")
    user = User(email="flight@example.com", full_name="Flight User", hashed_password=hashed_password)
    test_db.add(user)
    test_db.commit()
    
    login_response = client.post(
        "/api/auth/login",
        data={"username": "flight@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Test flight search
    response = client.post(
        "/api/search/flights",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "origin": "JFK",
            "destination": "LAX",
            "departureDate": "2023-12-01",
            "returnDate": "2023-12-05",
            "passengers": 2,
            "filters": {
                "priceRange": {"min": 200, "max": 1000},
                "airlines": ["Delta", "United"],
                "maxStops": 1
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "flights" in data
    assert isinstance(data["flights"], list)
    assert "total" in data

def test_search_experiences(client, test_db):
    """Test experiences search endpoint"""
    # Create a user and get authentication token
    hashed_password = get_password_hash("password123")
    user = User(email="exp@example.com", full_name="Experience User", hashed_password=hashed_password)
    test_db.add(user)
    test_db.commit()
    
    login_response = client.post(
        "/api/auth/login",
        data={"username": "exp@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Test experiences search
    response = client.post(
        "/api/search/experiences",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "location": "Paris",
            "dates": ["2023-12-01", "2023-12-02"],
            "participants": 2,
            "filters": {
                "priceRange": {"min": 50, "max": 200},
                "categories": ["Culture", "Food"],
                "duration": "3 hours",
                "languages": ["English"]
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "experiences" in data
    assert isinstance(data["experiences"], list)
    assert "total" in data