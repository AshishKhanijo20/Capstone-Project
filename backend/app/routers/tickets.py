from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlmodel import Session

from app.database.session import engine
from app.schemas.tickets import TicketCreate, TicketUpdate, TicketResponse
from app.crud.tickets import (
    create_ticket,
    get_ticket,
    get_all_tickets,
    update_ticket,
    assign_ticket,
    close_ticket
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


# Dependency
def get_session():
    with Session(engine) as session:
        yield session


# -------------------------------
# Create Ticket
# -------------------------------
@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_new_ticket(
    ticket_data: TicketCreate,
    opened_by_id: Optional[str] = None,
    session: Session = Depends(get_session)
):
    ticket = create_ticket(
        session=session,
        ticket_data=ticket_data,
        opened_by_id=opened_by_id
    )
    return ticket


# -------------------------------
# Get all tickets
# -------------------------------
@router.get("/", response_model=List[TicketResponse])
def read_all_tickets(
    session: Session = Depends(get_session)
):
    return get_all_tickets(session)


# -------------------------------
# Get single ticket
# -------------------------------
@router.get("/{ticket_id}", response_model=TicketResponse)
def read_ticket(
    ticket_id: str,
    session: Session = Depends(get_session)
):
    ticket = get_ticket(session, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


# -------------------------------
# Update ticket (generic)
# -------------------------------
@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket_details(
    ticket_id: str,
    ticket_update: TicketUpdate,
    session: Session = Depends(get_session)
):
    ticket = update_ticket(session, ticket_id, ticket_update)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


# -------------------------------
# Assign ticket
# -------------------------------
@router.post("/{ticket_id}/assign", response_model=TicketResponse)
def assign_ticket_to_user(
    ticket_id: str,
    assigned_to_id: str,
    session: Session = Depends(get_session)
):
    ticket = assign_ticket(session, ticket_id, assigned_to_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


# -------------------------------
# Close ticket
# -------------------------------
@router.post("/{ticket_id}/close", response_model=TicketResponse)
def close_ticket_endpoint(
    ticket_id: str,
    resolution_notes: str,
    session: Session = Depends(get_session)
):
    ticket = close_ticket(session, ticket_id, resolution_notes)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
