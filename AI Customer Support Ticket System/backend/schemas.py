from pydantic import BaseModel
from typing import Optional


class TicketCreate(BaseModel):
    customer_message: str

class TicketResponse(BaseModel):
    id: int
    customer_message: str
    category: Optional[str] = None
    sentiment: Optional[str] = None
    priority_score: Optional[str] = None
    ai_reply_draft: Optional[str] = None

    class Config:
        from_attributes = True
