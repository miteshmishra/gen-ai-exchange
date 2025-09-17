from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Association table for trip members
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
