from app.models.ticket import Ticket
from app.models.user import User
from sqlmodel import Session
from datetime import datetime


def build_initial_ticket_context(ticket: Ticket, session: Session) -> str:
    """
    Builds initial ticket context for system message.
    This is called ONCE when chat is first initiated.
    """
    # Get user details
    opened_by = None
    assigned_to = None
    
    if ticket.opened_by_id:
        opened_by = session.get(User, ticket.opened_by_id)
    if ticket.assigned_to_id:
        assigned_to = session.get(User, ticket.assigned_to_id)
    
    # Calculate ticket age
    ticket_age = datetime.utcnow() - ticket.raised_on
    hours_open = int(ticket_age.total_seconds() / 3600)
    
    context = f"""
=== TICKET CONTEXT ===
You are assisting with the following IT support ticket:

Ticket ID: {ticket.ticket_id}
Status: {ticket.status}
Severity: {ticket.severity}
Opened: {ticket.raised_on.strftime('%Y-%m-%d %H:%M UTC')} ({hours_open} hours ago)

Reported By: {opened_by.name if opened_by else 'Unknown'} ({ticket.opened_by_id})
Assigned To: {assigned_to.name if assigned_to else 'Unassigned'}

Short Description: {ticket.short_description}

Detailed Description:
{ticket.long_description or 'No detailed description provided'}

Configuration Item: {ticket.config_item or 'Not specified'}

=== YOUR ROLE ===
- Help resolve this ticket efficiently
- Use the `rag_search` tool for company policies, documentation, and known solutions
- Use the `get_ticket_details` tool if the user mentions ticket has been updated or asks for current status
- Suggest troubleshooting steps based on the issue description
- If you need to escalate or can't resolve, explain why clearly
- Keep responses professional but friendly

=== IMPORTANT GUIDELINES ===
- Always reference the ticket ID when discussing solutions
- If the issue is resolved, suggest updating ticket status to "Resolved"
- If severity seems incorrect, flag it
- Document any troubleshooting steps for the ticket record
- When user says "refresh ticket details" or "ticket has been updated", use get_ticket_details tool
"""
    return context