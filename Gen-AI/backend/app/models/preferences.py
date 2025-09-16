from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

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
