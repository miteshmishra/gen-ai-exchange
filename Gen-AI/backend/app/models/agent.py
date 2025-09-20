from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class Experiment(BaseModel):
    id: Optional[int] = None
    feature_key: str
    variants: List[Dict[str, Any]]
    metrics: Optional[Dict[str, Any]] = None
    status: str
    start_date: datetime
    end_date: Optional[datetime] = None

class AgentAction(BaseModel):
    id: Optional[int] = None
    feature_key: str
    agent_type: str
    change_spec: Dict[str, Any]
    rationale: str
    status: str
    approvals: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None