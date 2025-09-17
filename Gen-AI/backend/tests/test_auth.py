import pytest
from fastapi.testclient import TestClient
from app.db.models import User
from app.routers.auth import get_password_hash

def test_register_user(client, test_db):
    """Test user registration endpoint"""
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "password123", "full_name": "Test User"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    
    # Check that user was added to database
    db_user = test_db.query(User).filter(User.email == "test@example.com").first()
    assert db_user is not None
    assert db_user.email == "test@example.com"
    assert db_user.full_name == "Test User"

def test_register_existing_user(client, test_db):
    """Test registering a user with an email that already exists"""
    # Create a user first
    hashed_password = get_password_hash("password123")
    user = User(email="existing@example.com", full_name="Existing User", hashed_password=hashed_password)
    test_db.add(user)
    test_db.commit()
    
    # Try to register with the same email
    response = client.post(
        "/api/auth/register",
        json={"email": "existing@example.com", "password": "password123", "full_name": "New User"}
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_login_user(client, test_db):
    """Test user login endpoint"""
    # Create a user first
    hashed_password = get_password_hash("password123")
    user = User(email="login@example.com", full_name="Login User", hashed_password=hashed_password)
    test_db.add(user)
    test_db.commit()
    
    # Login with correct credentials
    response = client.post(
        "/api/auth/login",
        data={"username": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_db):
    """Test login with wrong password"""
    # Create a user first
    hashed_password = get_password_hash("password123")
    user = User(email="login@example.com", full_name="Login User", hashed_password=hashed_password)
    test_db.add(user)
    test_db.commit()
    
    # Login with wrong password
    response = client.post(
        "/api/auth/login",
        data={"username": "login@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_get_current_user(client, test_db):
    """Test getting current user information"""
    # Create a user first
    hashed_password = get_password_hash("password123")
    user = User(email="current@example.com", full_name="Current User", hashed_password=hashed_password)
    test_db.add(user)
    test_db.commit()
    
    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        data={"username": "current@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Get current user with token
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "current@example.com"
    assert data["full_name"] == "Current User"