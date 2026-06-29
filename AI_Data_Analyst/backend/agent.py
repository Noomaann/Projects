import os
import pandas as pd
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv(override=True)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.prompts import PromptTemplate

from backend.database import SQLALCHEMY_DATABASE_URL, engine

def ask_database(query: str):
    db = SQLDatabase.from_uri(SQLALCHEMY_DATABASE_URL)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0) 
    
    schema = db.get_table_info()
    prompt = PromptTemplate.from_template(
        "You are a smart Data Analyst. Database schema:\n{schema}\n\n"
        "User Question: {query}\n\n"
        "Write a valid SQL query to answer this. Return ONLY the raw SQL query, without ```sql or any other text."
    )
    chain = prompt | llm
    
    try:
        response = chain.invoke({"schema": schema, "query": query})
        sql_query = response.content.replace("```sql", "").replace("```", "").strip()
        
        with engine.connect() as conn:
            result = conn.execute(text(sql_query)).fetchall()
        
        if not result:
            return "No data found for this query."
            
        if len(result) == 1 and len(result[0]) == 1:
            return f"**Answer:** {result[0][0]}"
        else:
            clean_result = [dict(row._mapping) for row in result[:10]]
            return f"**Result:** {clean_result}"
            
    except Exception as e:
        return f"Error: {str(e)}"


def get_chart_data(query: str):
    db = SQLDatabase.from_uri(SQLALCHEMY_DATABASE_URL)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    schema = db.get_table_info()
    
    prompt = PromptTemplate.from_template(
        "You are an expert Data Analyst. Here is the database schema:\n{schema}\n\n"
        "User Request: {query}\n\n"
        "Write a valid SQL query to generate data for a chart. \n"
        "CRITICAL RULES:\n"
        "1. Return ONLY the raw SQL query. No explanation, no markdown (do NOT add ```sql).\n"
        "2. The query MUST return EXACTLY TWO columns (one for the X-axis category, one for the Y-axis value). For example: SELECT diagnosis, AVG(area_mean) FROM data_table GROUP BY diagnosis.\n"
        "3. Limit the results to 15 rows max."
    )
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({"schema": schema, "query": query})
        sql_query = response.content.replace("```sql", "").replace("```", "").strip()
        
        with engine.connect() as conn:
            df = pd.read_sql(text(sql_query), conn)
        
        return {
            "success": True,
            "sql_query": sql_query,
            "data": df.to_dict(orient="records"),
            "columns": list(df.columns)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    

def generate_business_summary():
    db = SQLDatabase.from_uri(SQLALCHEMY_DATABASE_URL)

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    schema = db.get_table_info()
    prompt = PromptTemplate.from_template(
        "You are an expert Business Analyst. Here is the database schema of the uploaded dataset:\n{schema}\n\n"
        "Please write a professional 'Executive Data Summary' (around 3 paragraphs) explaining what kind of data this is, "
        "what key insights or predictions could potentially be derived from it, and how it could be useful for business or research. "
        "Format it nicely with headings and bullet points where appropriate."
    )
    chain = prompt | llm
    
    try:
        response = chain.invoke({"schema": schema})
        return {"success": True, "summary": response.content}
    except Exception as e:
        return {"success": False, "error": str(e)}