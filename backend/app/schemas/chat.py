from pydantic import BaseModel
from typing import List
from datetime import datetime


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    message: str


class ChatMessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    ticket_id: str
    thread_id: str
    messages: List[ChatMessageResponse]