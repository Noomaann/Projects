import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st
import requests
import plotly.express as px
import pandas as pd

BACKEND_URL = "http://backend:8000"

st.set_page_config(page_title="AI Data Analyst", layout="wide", page_icon="📊")

premium_ui_style = """
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(109.6deg, rgba(244,247,250,1) 11.2%, rgba(234,240,247,1) 91.1%); }
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%); }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: white !important; }

section[data-testid="stSidebar"] .stFileUploader {
    background-color: rgba(255, 255, 255, 0.95) !important;
    border-radius: 10px !important;
    padding: 15px !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
}
section[data-testid="stSidebar"] .stFileUploader * { color: #1e3c72 !important; }
[data-testid="stFileUploadDropzone"] { border: 2px dashed #8E54E9 !important; background-color: transparent !important; }
section[data-testid="stSidebar"] .stFileUploader button {
    background: #e9ecef !important; color: #1e3c72 !important; border: 1px solid #1e3c72 !important; font-weight: bold !important; border-radius: 5px !important;
}
section[data-testid="stSidebar"] .stFileUploader svg { fill: #8E54E9 !important; }

div.stButton > button {
    background: linear-gradient(135deg, #4776E6 0%, #8E54E9 100%);
    color: white !important; font-weight: 600; border-radius: 8px; border: none; padding: 0.6rem 1.2rem;
    box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08); transition: all 0.3s ease-in-out;
}
div.stButton > button:hover {
    transform: translateY(-2px); box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
    background: linear-gradient(135deg, #3b66d6 0%, #7d43db 100%);
}
.stTextInput > div > div > input { border-radius: 8px; border: 1px solid #c0ccda; }
div[data-testid="stInfo"] { background-color: white; border-left: 5px solid #8E54E9; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
</style>
"""
st.markdown(premium_ui_style, unsafe_allow_html=True)

st.title("📊 AI Data Analyst Agent")
st.markdown("Upload your CSV database and ask natural language questions to analyze data seamlessly.")
st.markdown("---")

with st.sidebar:
    st.header("📂 Upload Dataset")
    st.markdown('<p style="color: white; font-weight: bold;">Select a CSV file</p>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

    if uploaded_file is not None:
        if st.button("🚀 Upload & Connect to DB"):
            with st.spinner("Processing your data..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                response = requests.post(f"{BACKEND_URL}/upload-csv/", files=files)
                
                if response.status_code == 200:
                    st.success(f"Database Connected: {uploaded_file.name}!")
                    data = response.json()
                    st.info(f"Rows: {data.get('total_rows')} | Columns: {len(data.get('columns', []))}")
                else:
                    st.error("Failed to connect database.")


st.subheader("💬 Query & Visualize Your Data")
question = st.text_input("Ask anything or request a chart (e.g., 'Show a bar chart of area_mean vs diagnosis')")

col1, col2 = st.columns(2)
with col1:
    ask_btn = st.button("✨ Analyze Text")
with col2:
    chart_btn = st.button("📊 Generate Chart")

if ask_btn and question:
    with st.spinner("AI is analyzing the database..."):
        payload = {"question": question}
        response = requests.post(f"{BACKEND_URL}/ask/", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            raw_answer = data.get("answer", "")
            
            if isinstance(raw_answer, list) and len(raw_answer) > 0 and isinstance(raw_answer[0], dict):
                final_answer = raw_answer[0].get("text", str(raw_answer))
            else:
                final_answer = str(raw_answer)
            
            st.info(f"**AI Response:** \n\n {final_answer}")
        else:
            st.error("Sorry, the AI encountered an issue.")

if chart_btn and question:
    with st.spinner("AI is extracting data and building the chart..."):
        payload = {"question": question}
        response = requests.post(f"{BACKEND_URL}/generate-chart/", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                df = pd.DataFrame(result.get("data"))
                columns = result.get("columns")
                
                if len(df) > 0 and len(columns) >= 2:
                    x_col = columns[0]
                    y_col = columns[1]
                    
                    st.success("Chart Generated Successfully!")
                    fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}", template="plotly_white", color=x_col)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    with st.expander("View Raw Data & AI SQL Query"):
                        st.code(result.get("sql_query"), language="sql")
                        st.dataframe(df, use_container_width=True)
                else:
                    st.warning("Not enough data to generate a chart. Try asking a different question.")
            else:
                st.error(f"Error: {result.get('error')}")


st.markdown("---")
st.subheader("📄 Executive Business Report")
st.markdown("Generate a comprehensive AI report of your dataset and export it.")

if st.button("📑 Generate & Export Report"):
    with st.spinner("AI is analyzing the database schema and writing the report..."):
        response = requests.get(f"{BACKEND_URL}/generate-summary/")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                summary = result.get("summary")
                st.success("Report Generated Successfully!")
                
                with st.expander("Preview Executive Summary", expanded=True):
                    st.markdown(summary)
                
                st.download_button(
                    label="📥 Download Report as TXT",
                    data=summary,
                    file_name="AI_Data_Report.txt",
                    mime="text/plain"
                )
            else:
                st.error(f"Failed to generate report: {result.get('error')}")
        else:
            st.error("Backend error.")