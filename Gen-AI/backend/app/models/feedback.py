from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

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
