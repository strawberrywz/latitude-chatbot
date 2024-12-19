from fastapi import APIRouter, HTTPException
from models.message import MessageModel
from models.schema import MessageCreate, MessageResponse, FeedbackUpdate
from typing import List, Optional

router = APIRouter()

message_model = MessageModel()

@router.post("/messages", response_model=MessageResponse)
def create_message(message: MessageCreate):
    try:
        return message_model.create_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
