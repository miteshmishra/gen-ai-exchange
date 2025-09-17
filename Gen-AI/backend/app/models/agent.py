from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class AgentAction(Base):
    __tablename__ = "agent_actions"

    id = Column(Integer, primary_key=True, index=True)
    feature_key = Column(String)  # Feature being modified
    agent_type = Column(String)  # Observer, Strategist, Implementer, Governor
    change_spec = Column(JSON)  # Detailed changes to apply
    rationale = Column(String)  # Explanation for the change
    approvals = Column(JSON)  # List of approval signals
    status = Column(String)  # proposed, approved, applied, rolled-back
    rollback_spec = Column(JSON)  # How to revert changes
    metrics = Column(JSON)  # Performance metrics after change
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    feature_key = Column(String)
    variants = Column(JSON)  # Different versions being tested
    allocation = Column(JSON)  # Traffic allocation rules
    metrics = Column(JSON)  # Success metrics to track
    guardrails = Column(JSON)  # Safety and performance thresholds
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    status = Column(String)  # active, completed, terminated
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
