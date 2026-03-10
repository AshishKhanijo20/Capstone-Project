from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    message: str
    sentiment: str  # "positive" or "negative"
    thread_id: Optional[str] = None # Add this back


class ChatMessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    ticket_id: str
    thread_id: str
    messages: List[ChatMessageResponse]