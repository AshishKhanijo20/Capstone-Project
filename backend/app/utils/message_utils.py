from typing import List
from sqlmodel import Session, select
from datetime import datetime

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from app.models.ChatMessage import ChatMessage
from app.models.ticket import Ticket
from app.utils.ticket_context import build_initial_ticket_context


# -----------------------------
# Role ↔ LangChain conversion
# -----------------------------

def db_to_langchain(msg: ChatMessage) -> BaseMessage:
    if msg.role == "system":
        return SystemMessage(content=msg.content)
    elif msg.role == "user":
        return HumanMessage(content=msg.content)
    elif msg.role == "assistant":
        return AIMessage(content=msg.content)
    else:
        raise ValueError(f"Unknown role: {msg.role}")


def langchain_to_db(
    message: BaseMessage,
    thread_id: str,
    ticket_id: str
) -> ChatMessage:
    if isinstance(message, HumanMessage):
        role = "user"
    elif isinstance(message, AIMessage):
        role = "assistant"
    elif isinstance(message, SystemMessage):
        role = "system"
    else:
        raise ValueError("Unsupported message type")

    return ChatMessage(
        thread_id=thread_id,
        ticket_id=ticket_id,
        role=role,
        content=message.content,
        created_at=datetime.utcnow()
    )


# -----------------------------
# Load conversation state
# -----------------------------

def load_conversation(
    session: Session,
    ticket: Ticket
) -> List[BaseMessage]:
    """
    Load chat history for a ticket.
    If no history exists, inject initial SYSTEM context.
    """

    stmt = (
        select(ChatMessage)
        .where(ChatMessage.thread_id == ticket.thread_id)
        .order_by(ChatMessage.created_at)
    )

    records = session.exec(stmt).all()

    # First chat message ever → inject system context
    if not records:
        system_context = build_initial_ticket_context(ticket, session)

        system_msg = ChatMessage(
            thread_id=ticket.thread_id,
            ticket_id=ticket.ticket_id,
            role="system",
            content=system_context,
        )

        session.add(system_msg)
        session.commit()

        return [SystemMessage(content=system_context)]

    return [db_to_langchain(m) for m in records]


# -----------------------------
# Persist messages
# -----------------------------

def save_messages(
    session: Session,
    messages: List[BaseMessage],
    ticket: Ticket
) -> None:
    """
    Persist LangChain messages to DB.
    Assumes messages are in chronological order.
    """

    for msg in messages:
        db_msg = langchain_to_db(
            message=msg,
            thread_id=ticket.thread_id,
            ticket_id=ticket.ticket_id
        )
        session.add(db_msg)

    session.commit()
