from fastapi import FastAPI
from app.database import engine, Base
from app.models.lead import Lead 
from app.routes.lead_routes import router as lead_router 


Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Lead Generation Agent")


app.include_router(lead_router)

@app.get("/")
def read_root():
    return {"message": "AI Lead Agent Backend is running successfully!"}