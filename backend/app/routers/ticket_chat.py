from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from langchain_core.messages import HumanMessage, SystemMessage

from app.database.session import get_session
from app.models.ticket import Ticket
from app.schemas.chat import ChatRequest, ChatResponse
from app.chatbot.agent import chatbot
from app.utils.message_utils import (
    load_conversation,
    save_messages,
)

router = APIRouter(prefix="/tickets", tags=["Ticket Chat"])


@router.post("/{ticket_id}/chat", response_model=ChatResponse)
def chat_with_ticket(
    ticket_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session),
):
    # 1️⃣ Load ticket
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # 2️⃣ Load conversation (system context auto-injected if first time)
    messages = load_conversation(session, ticket)

    # 3️⃣ Append user message
    user_msg = HumanMessage(content=request.message)
    messages.append(user_msg)
    save_messages(session, [user_msg], ticket)

    # 4️⃣ Run LangGraph (STATELESS)
    result = chatbot.invoke(
        {"messages": messages},
        config={
            "run_name": f"Ticket_{ticket_id}_Chat",  # Shows in LangSmith UI
            "tags": ["ticket-chat", ticket_id, ticket.severity, ticket.status],
            "metadata": {
                "ticket_id": ticket_id,
                "ticket_status": ticket.status,
                "ticket_severity": ticket.severity,
                "thread_id": ticket.thread_id,
                "message_count": len(messages),
            }
        }
        )   

    # 5️⃣ Persist only NEW messages
    new_messages = result["messages"][-1:]
    save_messages(session, new_messages, ticket)

    # 6️⃣ Respond
    ai_message = new_messages[0].content
    return ChatResponse(
        message=ai_message,
        thread_id=ticket.thread_id
    )


@router.get("/{ticket_id}/chat-history")
def get_chat_history(
    ticket_id: str,
    session: Session = Depends(get_session)
):
    # 1️⃣ Load ticket
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # 2️⃣ Load conversation from DB
    messages = load_conversation(session, ticket)

    # 3️⃣ Serialize messages (skip system messages)
    serialized = []
    for msg in messages:
        if isinstance(msg, SystemMessage):
            continue

        role = (
            "user" if isinstance(msg, HumanMessage)
            else "assistant"
        )

        serialized.append({
            "role": role,
            "content": msg.content
        })

    return {"messages": serialized}