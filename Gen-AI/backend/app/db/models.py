from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, JSON, Boolean, Float, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
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
    owned_trips = relationship("Trip", back_populates="owner")
    member_trips = relationship("Trip", secondary="trip_members", back_populates="members")
    feedback = relationship("Feedback", back_populates="user")

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
    user_id = Column(Integer, ForeignKey("users.id"))
    
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
    
    # Notification Preferences
    email_notifications = Column(Boolean, default=True)
    price_alerts = Column(Boolean, default=True)
    deal_notifications = Column(Boolean, default=True)
    
    # Currency and Language
    preferred_currency = Column(String, default="USD")
    preferred_language = Column(String, default="en")
    
    # Accessibility
    accessibility_needs = Column(JSON, default=list)    # List of accessibility requirements
    
    user = relationship("User", back_populates="preferences")

trip_members = Table(
    'trip_members',
    Base.metadata,
    Column('trip_id', Integer, ForeignKey('trips.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    origin = Column(String)
    destinations = Column(JSON)  # List of destinations
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    policy_context = Column(JSON)  # Travel policies and restrictions
    status = Column(String)  # planning, confirmed, in-progress, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="owned_trips")
    members = relationship("User", secondary=trip_members, back_populates="member_trips")
    itinerary_items = relationship("ItineraryItem", back_populates="trip")
    feedback = relationship("Feedback", back_populates="trip")

class ItineraryItem(Base):
    __tablename__ = "itinerary_items"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    type = Column(String)  # flight, hotel, activity, transport
    provider = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String)
    price_breakdown = Column(JSON)  # Detailed price components
    alt_options = Column(JSON)  # Alternative options
    compliance_flags = Column(JSON)  # Any compliance or safety flags
    weather_info = Column(JSON)  # Weather forecast for outdoor activities
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    trip = relationship("Trip", back_populates="itinerary_items")
    feedback = relationship("Feedback", back_populates="itinerary_item")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    itinerary_item_id = Column(Integer, ForeignKey("itinerary_items.id"), nullable=True)
    subject_type = Column(String)  # UI component, itinerary suggestion, etc.
    variant_id = Column(String, nullable=True)  # For A/B testing
    rating = Column(Float)  # 1-5 rating
    comment = Column(String, nullable=True)
    task_time_ms = Column(Integer, nullable=True)  # Time to complete task
    screen_reader_notes = Column(String, nullable=True)  # Accessibility feedback
    locale = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="feedback")
    trip = relationship("Trip", back_populates="feedback")
    itinerary_item = relationship("ItineraryItem", back_populates="feedback")