from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas
from nlp_utils import analyze_ticket  # নতুন ইম্পোর্ট

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Customer Support Ticket API",
    description="API for Ticket Classification and Auto Reply",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Customer Support Ticket API! Database connected successfully."}

@app.post("/tickets/", response_model=schemas.TicketResponse)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    
    # NLP মডেল দিয়ে মেসেজ এনালাইসিস করা
    analysis = analyze_ticket(ticket.customer_message)
    
    # এনালাইসিস করা ডেটা দিয়ে ডাটাবেসে সেভ করা
    new_ticket = models.Ticket(
        customer_message=ticket.customer_message,
        category=analysis["category"],
        sentiment=analysis["sentiment"],
        priority_score=analysis["priority_score"],
        ai_reply_draft=analysis["ai_reply_draft"]  # <-- এই লাইনটি যোগ করা হয়েছে
    )
    
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    
    return new_ticket




from typing import List  # একদম উপরের দিকে ইম্পোর্টের জায়গায় এটি যোগ করুন

# ... আপনার আগের কোডগুলো ...

# নতুন API: সব টিকিট ফেচ (Fetch) করার জন্য
@app.get("/tickets/all", response_model=List[schemas.TicketResponse])
def get_all_tickets(db: Session = Depends(get_db)):
    # ডাটাবেস থেকে সব টিকিট নিয়ে আসবে, লেটেস্ট টিকিটগুলো আগে দেখাবে
    tickets = db.query(models.Ticket).order_by(models.Ticket.id.desc()).all()
    return tickets