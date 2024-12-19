from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import requests
from config import settings

router = APIRouter()

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

chat_history: List[Message] = []

class FlowRequest(BaseModel):
    message: str
    endpoint: str = settings.FLOW_ID
    output_type: str = "chat"
    input_type: str = "chat"
    tweaks: Optional[Dict[str, Any]] = settings.DEFAULT_TWEAKS
    api_key: Optional[str] = None

def format_chat_history(history: List[Message]) -> str:
    """Format chat history into a single string."""
    formatted_history = ""
    for msg in history:
        formatted_history += f"{msg.role.capitalize()}: {msg.content}\n"
    return formatted_history

def run_flow(message: str,
             chat_history: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             api_key: Optional[str] = None) -> dict:
    """Run a flow with chat history and message."""
    api_url = f"{settings.BASE_API_URL}/api/v1/run/{endpoint}"
    
    full_message = f"{chat_history}Human: {message}\nAssistant:"
    
    payload = {
        "input_value": full_message,
        "output_type": output_type,
        "input_type": input_type,
    }
    used_api_key = api_key or settings.API_KEY
    headers = {"x-api-key": used_api_key} if used_api_key else None
    
    if tweaks:
        payload["tweaks"] = tweaks
        
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling Langflow API: {str(e)}")

@router.post("/run-flow")
async def run_flow_endpoint(request: FlowRequest):
    """Run a Langflow flow with chat history."""
    try:
        history_text = format_chat_history(chat_history)
        
        result = run_flow(
            message=request.message,
            chat_history=history_text,
            endpoint=request.endpoint,
            output_type=request.output_type,
            input_type=request.input_type,
            tweaks=request.tweaks,
            api_key=request.api_key or settings.API_KEY
        )
        
        assistant_response = result["outputs"][0]["outputs"][0]["artifacts"]["message"]
        
        chat_history.append(Message(role="user", content=request.message))
        chat_history.append(Message(role="assistant", content=assistant_response))
        
        return {"message": assistant_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat-history")
async def get_chat_history():
    """Get the complete chat history."""
    return {"history": chat_history}

@router.delete("/chat-history")
async def clear_chat_history():
    """Clear the chat history."""
    chat_history.clear()
    return {"message": "Chat history cleared"}

@router.get("/health")
async def health_check():
    """Check if the API is running and can connect to Langflow."""
    try:
        response = requests.get(f"{settings.BASE_API_URL}/health")
        response.raise_for_status()
        return {"status": "healthy", "langflow_status": "connected"}
    except requests.exceptions.RequestException:
        return {
            "status": "healthy",
            "langflow_status": "disconnected",
            "message": "Unable to connect to Langflow API"
        }