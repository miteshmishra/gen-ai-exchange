import pytest
from fastapi.testclient import TestClient
from app.db.models import User
from app.routers.auth import get_password_hash

def test_register_user(client, test_db_session, user_data):
    """Test user registration endpoint"""
    response = client.post(
        "/api/auth/register",
        json=user_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    
    # Check that user was added to database
    db_user = test_db_session.query(User).filter(User.email == user_data["email"]).first()
    assert db_user is not None
    assert db_user.email == user_data["email"]
    assert db_user.full_name == user_data["full_name"]

def test_register_existing_user(client, test_db_session, user_data):
    """Test registering a user with an email that already exists"""
    # Create a user first
    hashed_password = get_password_hash(user_data["password"])
    user = User(email=user_data["email"], full_name=user_data["full_name"], hashed_password=hashed_password)
    test_db_session.add(user)
    test_db_session.commit()
    
    # Try to register with the same email
    response = client.post(
        "/api/auth/register",
        json=user_data
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_login_user(client, test_db_session, user_data):
    """Test user login endpoint"""
    # Create a user first
    hashed_password = get_password_hash(user_data["password"])
    user = User(email=user_data["email"], full_name=user_data["full_name"], hashed_password=hashed_password)
    test_db_session.add(user)
    test_db_session.commit()
    
    # Login with correct credentials
    response = client.post(
        "/api/auth/login",
        data={"username": user_data["email"], "password": user_data["password"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_db_session, user_data):
    """Test login with wrong password"""
    # Create a user first
    hashed_password = get_password_hash(user_data["password"])
    user = User(email=user_data["email"], full_name=user_data["full_name"], hashed_password=hashed_password)
    test_db_session.add(user)
    test_db_session.commit()
    
    # Login with wrong password
    response = client.post(
        "/api/auth/login",
        data={"username": user_data["email"], "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_get_current_user(client, test_db_session, user_data):
    """Test getting current user information"""
    # Create a user first
    hashed_password = get_password_hash(user_data["password"])
    user = User(email=user_data["email"], full_name=user_data["full_name"], hashed_password=hashed_password)
    test_db_session.add(user)
    test_db_session.commit()
    
    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        data={"username": user_data["email"], "password": user_data["password"]}
    )
    token = login_response.json()["access_token"]
    
    # Get current user with token
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]