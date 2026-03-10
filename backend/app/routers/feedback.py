from app.schemas.feedback import FeedbackRequest
from fastapi import APIRouter, Depends
from app.database.session import get_session
from app.models.feedback import Feedback
from sqlmodel import Session

router = APIRouter(prefix="/feedback", tags=["Chat Feedback"])

@router.post("/")
def submit_feedback(
    feedback: FeedbackRequest,
    session: Session = Depends(get_session)
):
    """Submit feedback for a chatbot response"""
    new_feedback = Feedback(
        ticket_id=feedback.ticket_id,
        rating=feedback.rating,
        ai_response=feedback.ai_response,
        user_query=feedback.user_query,
        sentiment=feedback.sentiment
    )
    
    session.add(new_feedback)
    session.commit()
    session.refresh(new_feedback)
    
    return {"success": True, "message": "Thank you for your feedback!"}