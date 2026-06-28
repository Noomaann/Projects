from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime
from database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    customer_message = Column(Text, nullable=False)
    
    # AI Predictions (AI মডেল থেকে পাওয়া ডেটা)
    category = Column(String, index=True, nullable=True) # যেমন: Refund, Pricing, Technical Issue
    sentiment = Column(String, nullable=True)            # যেমন: Positive, Negative, Neutral
    priority_score = Column(String, nullable=True)       # যেমন: High, Medium, Low
    
    # Auto Reply Draft
    ai_reply_draft = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=False)         # অ্যাডমিন রিপ্লাই অ্যাপ্রুভ করেছে কিনা
    
    # Time Tracking
    created_at = Column(DateTime, default=datetime.utcnow)