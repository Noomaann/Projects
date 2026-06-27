from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LeadBase(BaseModel):
    name: str
    email: str
    company: Optional[str] = None
    job_title: Optional[str] = None
    linkedin_url: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadResponse(LeadBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True