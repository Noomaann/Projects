from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.database import get_db
from app.models.lead import Lead
from app.schemas import LeadCreate, LeadResponse
from app.services.llm_generator import email_generator
from app.services.scraper import get_company_info
from app.services.memory import memory_agent
from app.services.email_sender import send_email


router = APIRouter(prefix="/leads", tags=["Leads"])


class EmailPayload(BaseModel):
    email_content: str

@router.post("/", response_model=LeadResponse)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    db_lead = db.query(Lead).filter(Lead.email == lead.email).first()
    if db_lead:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_lead = Lead(**lead.dict())
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    
    if new_lead.company:
        try:
            company_details = get_company_info(new_lead.company)
            memory_agent.add_lead_context(
                lead_id=new_lead.id, 
                context_text=f"Company: {new_lead.company}. Info from web: {company_details}"
            )
            new_lead.context_data = str(company_details)
            db.commit()
        except Exception as e:
            print(f"Warning: Could not fetch web info for {new_lead.company}. Error: {e}")
            
    return new_lead


@router.get("/", response_model=List[LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()
    return leads

@router.post("/{lead_id}/generate-email")
def generate_email_for_lead(lead_id: int, db: Session = Depends(get_db)):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    lead_data = {
        "name": db_lead.name,
        "company": db_lead.company,
        "job_title": db_lead.job_title
    }
    
    generated_email = email_generator.generate_email(lead_data=lead_data, lead_id=lead_id)
    return {"lead_id": lead_id, "generated_email": generated_email}


@router.post("/{lead_id}/send-email")
def send_email_to_lead(lead_id: int, payload: EmailPayload, db: Session = Depends(get_db)):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    success, message = send_email(to_email=db_lead.email, email_content=payload.email_content)
    if not success:
        raise HTTPException(status_code=500, detail=message)

    db_lead.status = "emailed"
    db.commit()
    return {"message": "Email sent successfully!"}