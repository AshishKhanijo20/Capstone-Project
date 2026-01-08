from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TicketCreate(BaseModel):
    short_description: str
    long_description: str
    severity: str = 'Medium'
    #category: Optional[str] = 'General'
    config_item : Optional[str] = None


class TicketUpdate(BaseModel):
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    severity: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    assigned_to_id: Optional[str] = None
    resolution_notes: Optional[str] = None

class TicketResponse(BaseModel):
    ticket_id: str
    short_description: str
    long_description: Optional[str]
    severity: str
    #ategory: Optional[str]
    status: str
    raised_on: datetime
    updated_at: datetime
    thread_id: Optional[str]
    opened_by_id: Optional[str]
    assigned_to_id: Optional[str]