from pydantic import BaseModel
from typing import Optional

# কাস্টমার যখন মেসেজ পাঠাবে, তখন শুধু এই ডেটাটুকু আসবে
class TicketCreate(BaseModel):
    customer_message: str

# API থেকে রেসপন্স হিসেবে আমরা যা ফেরত পাঠাব
class TicketResponse(BaseModel):
    id: int
    customer_message: str
    category: Optional[str] = None
    sentiment: Optional[str] = None
    priority_score: Optional[str] = None
    ai_reply_draft: Optional[str] = None

    class Config:
        from_attributes = True