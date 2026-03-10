from langchain_core.tools import tool
from sqlmodel import Session
from app.models.ticket import Ticket
from app.database.session import engine
import json

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
        
'''
@tool
def suggest_ticket_status_update(
    ticket_id: str,
    new_status: str,
    reason: str
) -> str:
    """
    Suggest updating a ticket's status to the user. This requires user confirmation.
    Use this when the issue is resolved or needs status change.
    
    Valid statuses: Open, In Progress, Resolved, Closed
    
    Args:
        ticket_id: The ticket ID to update
        new_status: Suggested new status (Open, In Progress, Resolved, Closed)
        reason: Clear explanation of why this status change is recommended
    
    Returns:
        A structured suggestion that will be shown to the user for confirmation
    """
    # Validate status
    valid_statuses = ["Open", "In Progress", "Resolved", "Closed"]
    if new_status not in valid_statuses:
        return f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
    
    # Return a JSON-like suggestion that frontend can parse
    suggestion = {
        "type": "ticket_update_suggestion",
        "ticket_id": ticket_id,
        "proposed_status": new_status,
        "reason": reason
    }
    
    # Return formatted message with embedded JSON
    return f"""TICKET_UPDATE_SUGGESTION: {json.dumps(suggestion)}

I recommend changing the status of ticket {ticket_id} to '{new_status}'.

Reason: {reason}

Would you like me to proceed with this update?"""

'''


@tool
def suggest_ticket_status_update(
    ticket_id: str,
    new_status: str,
    reason: str,
    resolution_summary: str = None  # ← ADD THIS
) -> str:
    """
    Suggest updating a ticket's status to the user. This requires user confirmation.
    Use this when the issue is resolved or needs status change.
    
    Valid statuses: Open, In Progress, Resolved, Closed
    
    Args:
        ticket_id: The ticket ID to update
        new_status: Suggested new status (Open, In Progress, Resolved, Closed)
        reason: Clear explanation of why this status change is recommended
        resolution_summary: Brief summary of how the issue was resolved (used for resolution notes)
    
    Returns:
        A structured suggestion that will be shown to the user for confirmation
    """
    valid_statuses = ["Open", "In Progress", "Resolved", "Closed"]
    if new_status not in valid_statuses:
        return f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
    
    suggestion = {
        "type": "ticket_update_suggestion",
        "ticket_id": ticket_id,
        "proposed_status": new_status,
        "reason": reason,
        "resolution_summary": resolution_summary or reason  # Use reason if no summary provided
    }
    
    return f"TICKET_UPDATE_SUGGESTION: {json.dumps(suggestion)}"