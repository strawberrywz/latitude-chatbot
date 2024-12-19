from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    message: str
    feedback: Optional[str] = None

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: str
    timestamp: datetime

class FeedbackUpdate(BaseModel):
    feedback: str  # "like" or "dislike"