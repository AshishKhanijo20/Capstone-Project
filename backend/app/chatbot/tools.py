from langchain_core.tools import tool
from sqlmodel import Session
from app.models.ticket import Ticket
from app.database.session import engine

@tool
def refresh_ticket_context (ticket_id: str)-> str:
    """
    Retrieve the latest ticket information when ticket details have been updated.
    Use this tool when you need to see current ticket status, description, or resolution notes.
    
    Args:
        ticket_id: The ticket ID (e.g., INC000001)
    
    Returns:
        Current ticket details including status, description, resolution notes
    """
    with Session(engine) as session:
        ticket = session.get(Ticket, ticket_id)

        if not ticket:
            return f"Ticket with ID {ticket_id} not found."
        
        return f"""
CURRENT TICKET DETAILS:
- Ticket ID: {ticket.ticket_id}
- Status: {ticket.status}
- Severity: {ticket.severity}
- Short Description: {ticket.short_description}
- Detailed Description: {ticket.long_description or 'Not provided'}
- Resolution Notes: {ticket.resolution_notes or 'Not yet resolved'}
- Opened By: {ticket.opened_by_id or 'Unknown'}
- Assigned To: {ticket.assigned_to_id or 'Unassigned'}
- Last Updated: {ticket.updated_at}
"""
        

    


