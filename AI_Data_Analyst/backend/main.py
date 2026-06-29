from fastapi import FastAPI, UploadFile, File
import pandas as pd
from backend.database import engine
from pydantic import BaseModel
from backend.agent import ask_database, get_chart_data, generate_business_summary

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    df.to_sql("data_table", engine, if_exists="replace", index=False)
    return {"message": "File uploaded successfully", "columns": list(df.columns), "total_rows": len(df)}

@app.post("/ask/")
async def ask(request: QuestionRequest):
    answer = ask_database(request.question)
    return {"answer": answer}

@app.post("/generate-chart/")
async def generate_chart(request: QuestionRequest):
    return get_chart_data(request.question)


@app.get("/generate-summary/")
async def get_summary():
    return generate_business_summary()