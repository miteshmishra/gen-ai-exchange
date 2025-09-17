from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

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
