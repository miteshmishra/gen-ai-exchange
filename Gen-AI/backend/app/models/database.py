from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    searches = relationship("SearchHistory", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False, cascade="all, delete-orphan")

class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    search_type = Column(String)  # hotel, flight, experience
    query = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="searches")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    item_type = Column(String)  # hotel, flight, experience
    item_id = Column(String)
    item_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    
    # Travel Style
    travel_style = Column(String)
    preferred_activities = Column(ARRAY(String), default=list)

    # Accommodation
    room_type = Column(String)
    max_price_per_night = Column(Float)
    preferred_amenities = Column(ARRAY(String), default=list)

    # Flight
    seat_preference = Column(String)
    cabin_class = Column(String)

    # Notifications
    email_notifications = Column(Boolean, default=True)
    price_alerts = Column(Boolean, default=True)
    deal_notifications = Column(Boolean, default=True)

    # Regional
    preferred_currency = Column(String, default="USD")
    preferred_language = Column(String, default="en")

    # Accessibility
    accessibility_needs = Column(ARRAY(String), default=list)

    # Relationship
    user = relationship("User", back_populates="preferences")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_type = Column(String)  # hotel, flight, experience
    item_id = Column(String)
    item_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="favorites")
