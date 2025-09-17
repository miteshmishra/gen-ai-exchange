from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings
from ..models.database import Base

# Import additional models to ensure they are included in database schema
from ..models import trips, itinerary, feedback, preferences

SQLALCHEMY_DATABASE_URL = "postgresql://travel_user:travel_password@localhost:5432/travel_hub"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
