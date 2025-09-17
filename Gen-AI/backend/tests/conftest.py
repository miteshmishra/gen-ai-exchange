<<<<<<< HEAD
=======
import sys
import os
>>>>>>> 4b2314a6cc56681354d2303eda9c8b811f673e73
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

<<<<<<< HEAD
from app.core.config import settings
from app.db.session import get_db
from app.main import app


@pytest.fixture(scope="session")
def test_db_engine():
    """Create a test database engine with SQLite in memory."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """Create a fresh database session for each test."""
    from app.db.models import Base
    
    # Create all tables
    Base.metadata.create_all(bind=test_db_engine)
    
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_db_engine
    )
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_db_engine)


@pytest.fixture(scope="function")
def client(test_db_session):
    """Create a test client with the test database session."""
    
    def override_get_db():
        try:
            yield test_db_session
=======
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
>>>>>>> 4b2314a6cc56681354d2303eda9c8b811f673e73
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
<<<<<<< HEAD
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
=======
    with TestClient(app) as c:
        yield c
    # Reset the dependency override after the test
    app.dependency_overrides = {}
>>>>>>> 4b2314a6cc56681354d2303eda9c8b811f673e73
