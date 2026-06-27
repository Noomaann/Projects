from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base
from datetime import datetime

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    company = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    

    status = Column(String, default="new") 
    
    context_data = Column(Text, nullable=True) 
    
    created_at = Column(DateTime, default=datetime.utcnow)