from app.models.ticket import Ticket, generate_ticket_id
import uuid
import datetime
from sqlmodel import Session , select
from typing import Optional, List
from app.schemas.tickets import TicketCreate, TicketUpdate

def create_ticket(
        session: Session,
        ticket_data : TicketCreate,
        opened_by_id: Optional[str] = None,
        thread_id : Optional[str] = None
) -> Ticket:
    ticket_id = generate_ticket_id(session)

    if not thread_id:
        thread_id = str(uuid.uuid4())
    
    ticket = Ticket(
        ticket_id=ticket_id,
        short_description=ticket_data.short_description,
        long_description=ticket_data.long_description,
        severity=ticket_data.severity,
        #category=ticket_data.category,
        config_item=ticket_data.config_item,
        opened_by_id=opened_by_id,
        thread_id=thread_id,
        #ai_suggestion=ai_suggestion,
        status="Open"
    )

    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket


def get_ticket(session : Session, ticket_id : str) -> Optional[Ticket]:
    return session.exec(select(Ticket).where(Ticket.ticket_id == ticket_id)).first()

def get_all_tickets(session: Session, skip: int = 0, limit: int = 100) -> List[Ticket]:
    return session.exec(select(Ticket).offset(skip).limit(limit)).all()


def get_tickets_by_user(session: Session, user_id: str) -> List[Ticket]:
    return session.exec(select(Ticket).where(Ticket.opened_by_id == user_id)).all()


def get_tickets_by_status(session: Session, status: str) -> List[Ticket]:
    return session.exec(select(Ticket).where(Ticket.status == status)).all()


def update_ticket(session: Session, ticket_id: str, ticket_update: TicketUpdate) -> Optional[Ticket]:
    ticket = get_ticket(session, ticket_id)
    if not ticket:
        return None
    
    update_data = ticket_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ticket, key, value)
    
    ticket.updated_at = datetime.utcnow()
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket


def assign_ticket(session: Session, ticket_id: str, assigned_to_id: str) -> Optional[Ticket]:
    ticket = get_ticket(session, ticket_id)
    if not ticket:
        return None
    
    ticket.assigned_to_id = assigned_to_id
    ticket.status = "In Progress"
    ticket.updated_at = datetime.utcnow()
    
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket


def close_ticket(session: Session, ticket_id: str, resolution_notes: str) -> Optional[Ticket]:
    ticket = get_ticket(session, ticket_id)
    if not ticket:
        return None
    
    ticket.status = "Closed"
    ticket.resolution_notes = resolution_notes
    ticket.updated_at = datetime.utcnow()
    
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket