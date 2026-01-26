from sqlmodel import SQLModel, Field, Relationship,Column,JSON, select
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Integer

if TYPE_CHECKING:
    from app.models.user import User


"""

def generate_ticket_id (session : Session):
    result = session.exec(
        select(func.max(cast(func.substr(Ticket.ticket_id,4),Integer)))
    ).one()

    max_number = result[0] or 0
    new_number = max_number + 1

    return f"INC{new_number:06d}"
"""

def generate_ticket_id(session: Session):
    result = session.exec(
        select(func.max(cast(func.substr(Ticket.ticket_id, 4), Integer)))
    ).one()

    max_number = int(result) if result is not None else 0
    return f"INC{max_number + 1:06d}"


class Ticket(SQLModel, table= True):
    ticket_id : str = Field(default =None,primary_key = True)
    severity : str = "Medium"
    opened_by_id : Optional[str] =  Field(default = None, foreign_key = "user.user_id")
    assigned_to_id : Optional[str]= Field(default = None, foreign_key = "user.user_id")
    raised_on: datetime = Field(default_factory = datetime.utcnow)
    short_description : str
    long_description : Optional[str] = None
    resolution_notes : Optional[str] = None
    config_item : Optional[str] = None
    chat_vector: Optional[dict] = Field(default = None,sa_column = Column(JSON))
    status : str = "Open"
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    thread_id: Optional[str] = Field(default=None, index=True)

    opened_by : Optional["User"] =  Relationship(
        back_populates = "tickets_created",sa_relationship_kwargs ={"foreign_keys":"[Ticket.opened_by_id]"}
    )
    assigned_to : Optional["User"] = Relationship(
        back_populates = "tickets_assigned", sa_relationship_kwargs = {"foreign_keys": "[Ticket.assigned_to_id]"}
    )