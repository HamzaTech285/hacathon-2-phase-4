"""Chat API router."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..database import get_session
from ..services.chat_service import ChatService
from ..auth_handler import get_current_user
from sqlmodel import Session

chat_router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    conversation_id: int
    response: str
    tool_calls: list


@chat_router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Chat endpoint for AI-powered task management.
    
    Accepts user messages and returns AI-generated responses.
    Maintains conversation history in the database.
    """
    try:
        chat_service = ChatService()
        user_id = current_user["user_id"]
        
        result = await chat_service.generate_response(
            session=session,
            user_id=user_id,
            user_message=request.message,
            conversation_id=request.conversation_id
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")
