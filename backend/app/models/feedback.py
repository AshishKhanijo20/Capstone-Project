from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Feedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: str = Field(foreign_key="ticket.ticket_id",index=True)
    # Simple data from the UI
    rating: int  # 1 to 5
    user_query: str  # What the user just said
    ai_response: str  # What the AI just said
    sentiment: str  # "positive" or "negative" (detected by your UI)
    created_at: datetime = Field(default_factory=datetime.utcnow)