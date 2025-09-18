from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    searches = relationship("Search", back_populates="user")
    preferences = relationship("UserPreference", back_populates="user")

class Search(Base):
    __tablename__ = "searches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    query = Column(String)
    search_type = Column(String)  # hotels, flights, or experiences
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="searches")

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Travel Preferences
    preferred_destinations = Column(JSON, default=list)  # List of favorite destinations
    preferred_activities = Column(JSON, default=list)    # List of activity types
    travel_style = Column(String)                       # luxury, budget, adventure, etc.
    
    # Accommodation Preferences
    preferred_amenities = Column(JSON, default=list)    # Must-have amenities
    room_type = Column(String)                         # single, double, suite
    max_price_per_night = Column(Integer)              # Budget limit per night
    
    # Flight Preferences
    preferred_airlines = Column(JSON, default=list)     # Preferred airlines
    seat_preference = Column(String)                   # window, aisle, no preference
    cabin_class = Column(String)                      # economy, business, first
    
    # Currency and Language
    preferred_currency = Column(String, default="USD")
    preferred_language = Column(String, default="en")
    
    # Accessibility
    accessibility_needs = Column(JSON, default=list)    # List of accessibility requirements
    
    # Notification Preferences
    email_notifications = Column(Boolean, default=True)
    price_alerts = Column(Boolean, default=True)
    deal_notifications = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="preferences")