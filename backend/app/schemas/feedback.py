from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    ticket_id: str 
    rating: int  
    user_query: str  
    ai_response: str  # What the AI just said
    sentiment: str  # "positive" or "negative" (detected by your UI)
    
    