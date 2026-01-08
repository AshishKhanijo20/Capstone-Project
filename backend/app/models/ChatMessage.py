from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    thread_id: str = Field(index=True)
    ticket_id: str = Field(index=True)

    role: str  # "system" | "user" | "assistant"
    content: str

    created_at: datetime = Field(default_factory=datetime.utcnow)