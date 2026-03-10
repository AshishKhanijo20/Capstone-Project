from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel

from app.database.session import get_session
from app.models.ticket import Ticket
from datetime import datetime

router = APIRouter(prefix="/tickets", tags=["Ticket Actions"])


class ConfirmUpdateRequest(BaseModel):
    new_status: str
    resolution_notes: str = None


@router.post("/{ticket_id}/confirm-update")
def confirm_ticket_update(
    ticket_id: str,
    request: ConfirmUpdateRequest,
    session: Session = Depends(get_session)
):
    """
    Execute a ticket update after user confirmation.
    """
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Update ticket
    ticket.status = request.new_status
    if request.resolution_notes:
        ticket.resolution_notes = request.resolution_notes
    ticket.updated_at = datetime.utcnow()
    
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    
    return {
        "success": True,
        "message": f"Ticket {ticket_id} updated to {request.new_status}",
        "ticket": {
            "ticket_id": ticket.ticket_id,
            "status": ticket.status,
            "resolution_notes": ticket.resolution_notes
        }
    }