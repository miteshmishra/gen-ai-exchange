import pytest
from fastapi.testclient import TestClient
from app.db.models import User, UserSearches
from app.routers.auth import get_password_hash

def test_get_user_analytics(client, test_db_session):
    """Test getting user analytics"""
    # Create a user and get authentication token
    hashed_password = get_password_hash("password123")
    user = User(email="analytics@example.com", full_name="Analytics User", hashed_password=hashed_password)
    test_db_session.add(user)
    test_db_session.commit()
    
    # Add some search history
    search1 = UserSearches(user_id=user.id, search_term="New York", search_type="hotels", location="New York")
    search2 = UserSearches(user_id=user.id, search_term="Paris", search_type="hotels", location="Paris")
    search3 = UserSearches(user_id=user.id, search_term="JFK to LAX", search_type="flights", location="United States")
    test_db_session.add_all([search1, search2, search3])
    test_db_session.commit()
    
    login_response = client.post(
        "/api/auth/login",
        data={"username": "analytics@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Test user analytics endpoint
    response = client.get(
        "/api/analytics/user",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "recent_searches" in data
    assert len(data["recent_searches"]) == 3
    assert "search_count_by_type" in data
    assert data["search_count_by_type"]["hotels"] == 2
    assert data["search_count_by_type"]["flights"] == 1

def test_get_search_analytics(client, test_db_session):
    """Test getting search analytics"""
    # Create an admin user
    hashed_password = get_password_hash("admin123")
    admin = User(email="admin@example.com", full_name="Admin User", hashed_password=hashed_password)
    test_db_session.add(admin)
    
    # Create regular users with searches
    user1 = User(email="user1@example.com", full_name="User One", hashed_password=hashed_password)
    user2 = User(email="user2@example.com", full_name="User Two", hashed_password=hashed_password)
    test_db_session.add_all([user1, user2])
    test_db_session.commit()
    
    # Add searches
    searches = [
        UserSearches(user_id=user1.id, search_term="New York", search_type="hotels", location="New York"),
        UserSearches(user_id=user1.id, search_term="Paris", search_type="hotels", location="Paris"),
        UserSearches(user_id=user2.id, search_term="JFK to LAX", search_type="flights", location="United States"),
        UserSearches(user_id=user2.id, search_term="London tours", search_type="experiences", location="London")
    ]
    test_db_session.add_all(searches)
    test_db_session.commit()
    
    # Login as admin
    login_response = client.post(
        "/api/auth/login",
        data={"username": "admin@example.com", "password": "admin123"}
    )
    token = login_response.json()["access_token"]
    
    # Test search analytics endpoint
    response = client.get(
        "/api/analytics/search",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "total_searches" in data
    assert data["total_searches"] == 4
    assert "searches_by_type" in data
    assert data["searches_by_type"]["hotels"] == 2
    assert data["searches_by_type"]["flights"] == 1
    assert data["searches_by_type"]["experiences"] == 1
    assert "popular_destinations" in data