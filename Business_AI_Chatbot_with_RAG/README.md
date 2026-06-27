<div align="center">

# 🤖 Business AI Chatbot
### RAG-Powered Document Assistant

**Upload your PDFs. Ask anything. Get instant, grounded answers.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

</div>

---

## 🌐 Live Demo

> No installation required — try it right now!

| Service | URL |
|---|---|
| 💬 **Chatbot Interface** | [projects-production-e786.up.railway.app](https://projects-production-e786.up.railway.app) |
| ⚡ **Backend API** | [just-freedom-production.up.railway.app](https://just-freedom-production.up.railway.app) |

**Quick start:**
1. Open the **Chatbot Interface** link above
2. Upload any PDF from the sidebar
3. Ask questions about your document in the chat!

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **PDF Upload & Indexing** | Auto-parses, chunks, embeds, and stores any uploaded business document |
| 🔍 **Semantic Search** | Vector similarity search via pgvector to find the most relevant sections |
| 🤖 **AI-Powered Answers** | Google Gemini 2.5 Flash generates context-aware, grounded responses |
| 🚫 **Hallucination-Free** | Strictly answers from the uploaded document; says *"Not found in document"* when unsure |
| 💬 **Streaming Chat UI** | Clean, real-time streaming interface built with Streamlit |
| 🐳 **Zero-Config Database** | PostgreSQL + pgvector runs via Docker Compose — no manual SQL setup |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Backend API** | FastAPI + Uvicorn |
| **LLM** | Google Gemini 2.5 Flash (`langchain-google-genai`) |
| **Embeddings** | Gemini Embedding 001 |
| **Vector Store** | PostgreSQL + pgvector |
| **RAG Framework** | LangChain |
| **PDF Parsing** | PyPDFLoader |
| **Containerization** | Docker Compose |

---

## 📁 Project Structure

```
business-ai-chatbot/
│
├── app.py                 # Streamlit frontend (chat UI + file uploader)
├── main.py                # FastAPI backend (chat & upload endpoints)
├── rag_pipeline.py        # Standalone ingestion script (PDF / Web loader)
├── check_models.py        # Utility to list available Gemini models
│
├── docker-compose.yml     # PostgreSQL + pgvector database setup
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
└── .gitignore
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- [Google API Key](https://aistudio.google.com/app/apikey)

### 1. Clone the Repository

```bash
git clone https://github.com/Noomaann/business-ai-chatbot.git
cd business-ai-chatbot
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
# Open .env and add your Google API key
```

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Start the Database

```bash
docker compose up -d
```

> Spins up a PostgreSQL 16 instance with pgvector on port **5433**.

### 4. Install Python Dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Run the Backend

```bash
uvicorn main:app --reload
```

> API available at `http://127.0.0.1:8000`

### 6. Run the Frontend

```bash
streamlit run app.py
```

> UI opens at `http://localhost:8501`

---

## 🔄 How It Works

```
User uploads PDF
      │
      ▼
FastAPI /upload endpoint
      │
      ▼
PyPDFLoader → RecursiveCharacterTextSplitter
         (800 tokens, 150 overlap)
      │
      ▼
Gemini Embedding 001 → pgvector (PostgreSQL)


User asks a question
      │
      ▼
FastAPI /chat endpoint
      │
      ▼
Query → Embed → Similarity Search (top 8 chunks)
      │
      ▼
Gemini 2.5 Flash → Grounded Answer
      │
      ▼
Streamlit UI (streaming response)
```

---

## 📡 API Reference

### `POST /upload`

Upload and index a PDF document.

**Request:** `multipart/form-data` with a `file` field (PDF)

**Response:**
```json
{
  "status": "success",
  "message": "Document processed and indexed successfully."
}
```

---

### `POST /chat`

Ask a question about the indexed documents.

**Request:**
```json
{
  "question": "What is the refund policy?"
}
```

**Response:**
```json
{
  "answer": "According to the document, the refund policy allows..."
}
```

---

## 🐳 Docker Compose

```yaml
services:
  db:
    image: pgvector/pgvector:pg16
    ports:
      - "5433:5432"
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: adminpassword
      POSTGRES_DB: rag_db
```

The app connects to this database automatically — no manual SQL setup needed.

---

## 🚀 Deployment

This project is designed for easy deployment on:

- **Railway** — Native pgvector PostgreSQL support; deploy backend & frontend as separate services
- **AWS EC2 / ECS** — Run Docker Compose directly on a VM
- **Render** — Deploy FastAPI and Streamlit as web services

> ⚠️ For production, replace hardcoded DB credentials with environment variables and use a managed PostgreSQL service with pgvector support.

---

## 🎯 Use Cases

| Use Case | Description |
|---|---|
| 📋 **HR Policy Bot** | Let employees query company handbooks |
| 🏥 **Medical Document Assistant** | Query clinical guidelines or reports |
| 📦 **Product Manual Bot** | Answer customer questions from product docs |
| ⚖️ **Legal Document Search** | Navigate contracts and legal filings |
| 📊 **Business Report Analyst** | Ask questions about financial reports |

---

## 📌 Environment Variables

| Variable | Description |
|---|---|
| `GOOGLE_API_KEY` | Your Google AI Studio / Gemini API key |

---

## 📜 License

This project is licensed under the **MIT License** — free to use, modify, and distribute. See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Abdul Kader Noman**

[![GitHub](https://img.shields.io/badge/GitHub-Noomaann-181717?style=flat-square&logo=github)](https://github.com/Noomaann)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com)

---

<div align="center">

⭐ **If you find this project useful, please give it a star!** ⭐

</div>
