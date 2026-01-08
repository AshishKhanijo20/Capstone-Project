from sqlmodel import SQLModel, Field, Relationship,Column,JSON, select
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Integer


if TYPE_CHECKING:
    from app.models.ticket import Ticket


def generate_user_id(session:Session):
    result = session.exec(
        select(func.max(cast(func.substr(User.user_id,4), Integer)))
    ).one()
    max_number = result[0] or 0
    new_number = max_number + 1
    return f"USR{new_number:06d}"


class User(SQLModel, table = True):
    user_id : str = Field(default = None, primary_key = True)
    username: str = Field(unique=True, index=True)
    hashed_password : str 
    name : str
    email : Optional[str] = None
    user_type : str = "Customer"
    created_at:datetime = Field(default_factory = datetime.utcnow)


    tickets_created: List["Ticket"] = Relationship(
        back_populates="opened_by",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.opened_by_id]"}
    )
    tickets_assigned: List["Ticket"] = Relationship(
        back_populates="assigned_to",
        sa_relationship_kwargs={"foreign_keys": "[Ticket.assigned_to_id]"}
    )