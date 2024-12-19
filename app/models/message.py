from datetime import datetime, timezone
from .database import Database
from .schema import MessageCreate, MessageResponse
from typing import Optional, Literal

class MessageModel:
    def __init__(self):
        self.db = Database.get_instance()
        self.messages = self.db.messages
    
    def create_message(self, message: MessageCreate) -> MessageResponse:
        current_time = datetime.now(timezone.utc)
        message_id = str(int(current_time.timestamp()))
        timestamp = current_time.isoformat()
        
        document = {
            "id": message_id,
            "message": message.message,
            "feedback": message.feedback,
            "timestamp": timestamp
        }
        
        self.messages.insert_one(document)
        
        return MessageResponse(
            id=message_id,
            message=message.message,
            feedback=message.feedback,
            timestamp=datetime.fromisoformat(timestamp)
        )
    
    def update_feedback(self, message_id: str, feedback: Literal['like', 'dislike']) -> bool:
        if feedback not in ['like', 'dislike']:
            raise ValueError("Feedback must be either 'like' or 'dislike'")
            
        result = self.messages.update_one(
            {"id": message_id},
            {"$set": {"feedback": feedback}}
        )
        return result.modified_count > 0
    
    def get_message(self, message_id: str) -> Optional[MessageResponse]:
        document = self.messages.find_one({"id": message_id})
        
        if not document:
            return None
            
        return MessageResponse(
            id=document["id"],
            message=document["message"],
            feedback=document.get("feedback"),
            timestamp=datetime.fromisoformat(document["timestamp"])
        )

    def get_messages_with_feedback(self, feedback: Optional[str] = None):
        """Get all messages with specific feedback or all messages if feedback is None"""
        query = {"feedback": feedback} if feedback else {}
        return list(self.messages.find(query))

    def get_feedback_stats(self):
        """Get statistics about feedback"""
        total = self.messages.count_documents({})
        likes = self.messages.count_documents({"feedback": "like"})
        dislikes = self.messages.count_documents({"feedback": "dislike"})
        no_feedback = self.messages.count_documents({"feedback": None})
        
        return {
            "total_messages": total,
            "likes": likes,
            "dislikes": dislikes,
            "no_feedback": no_feedback,
            "like_ratio": likes/total if total > 0 else 0
        }