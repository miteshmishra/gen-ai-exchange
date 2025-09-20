from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Feedback(BaseModel):
    id: Optional[int] = None
    user_id: int
    trip_id: Optional[int] = None
    itinerary_item_id: Optional[int] = None
    subject_type: str
    variant_id: Optional[str] = None
    rating: float
    comment: Optional[str] = None
    task_time_ms: Optional[int] = None
    screen_reader_notes: Optional[str] = None
    locale: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True