from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime
from database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    customer_message = Column(Text, nullable=False)
    
  
    category = Column(String, index=True, nullable=True) 
    sentiment = Column(String, nullable=True)            
    priority_score = Column(String, nullable=True)     
    

    ai_reply_draft = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=False)        
    

    created_at = Column(DateTime, default=datetime.utcnow)
