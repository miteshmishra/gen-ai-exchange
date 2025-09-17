import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock the database connection before importing app modules
import app.db.session
app.db.session.SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
app.db.session.engine = create_engine(
    app.db.session.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
app.db.session.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=app.db.session.engine)

from app.main import app
from app.models.database import Base
from app.db.session import get_db

@pytest.fixture(scope="function")
def test_db():
    # Create the database tables
    Base.metadata.create_all(bind=app.db.session.engine)
    db = app.db.session.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the test is complete
        Base.metadata.drop_all(bind=app.db.session.engine)

@pytest.fixture(scope="function")
def client(test_db):
    # Override the get_db dependency to use the test database
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Reset the dependency override after the test
    app.dependency_overrides = {}