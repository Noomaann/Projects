# 🚀 Business AI Chatbot — RAG-Powered Document Assistant

A production-ready **Retrieval-Augmented Generation (RAG)** chatbot that lets businesses upload their own PDF documents and instantly query them using natural language. Built with **FastAPI**, **Streamlit**, **LangChain**, **Google Gemini**, and **pgvector** on PostgreSQL.

---

## ✨ Features

- 📄 **PDF Upload & Indexing** — Upload any business document and the system automatically parses, chunks, embeds, and stores it
- 🔍 **Semantic Search** — Uses vector similarity search (pgvector) to find the most relevant document sections
- 🤖 **AI-Powered Answers** — Google Gemini 2.5 Flash generates context-aware, grounded responses
- 🚫 **Hallucination-Free** — Strictly answers from the uploaded document only; says "Not found in document" when unsure
- 💬 **Chat Interface** — Clean streaming chat UI built with Streamlit
- 🐳 **Dockerized Database** — PostgreSQL + pgvector runs via Docker Compose with zero manual setup

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit |
| **Backend API** | FastAPI + Uvicorn |
| **AI / LLM** | Google Gemini 2.5 Flash (`langchain-google-genai`) |
| **Embeddings** | Gemini Embedding 001 |
| **Vector Store** | PostgreSQL + pgvector |
| **RAG Framework** | LangChain |
| **PDF Parsing** | PyPDFLoader |
| **Containerization** | Docker Compose |

---

## 📁 Project Structure

```
├── app.py                 # Streamlit frontend (chat UI + file uploader)
├── main.py                # FastAPI backend (chat & upload endpoints)
├── rag_pipeline.py        # Standalone ingestion script (PDF / Web loader)
├── check_models.py        # Utility to list available Gemini models
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
- Google API Key ([Get one here](https://aistudio.google.com/))

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/business-ai-chatbot.git
cd business-ai-chatbot
```

### 2. Configure environment variables
```bash
cp .env.example .env
# Open .env and add your Google API key
```

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Start the PostgreSQL + pgvector database
```bash
docker compose up -d
```
This spins up a PostgreSQL 16 instance with pgvector on port `5433`.

### 4. Install Python dependencies
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Run the FastAPI backend
```bash
uvicorn main:app --reload
```
API will be live at `http://127.0.0.1:8000`

### 6. Run the Streamlit frontend
```bash
streamlit run app.py
```
UI will open at `http://localhost:8501`

---

## 🔄 How It Works

```
User uploads PDF
      │
      ▼
FastAPI /upload endpoint
      │
      ▼
PyPDFLoader → RecursiveCharacterTextSplitter (800 tokens, 150 overlap)
      │
      ▼
Gemini Embedding 001 → pgvector (PostgreSQL)
      │
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

## 📡 API Endpoints

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

## 🐳 Docker Compose Details

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

> The app connects to this database automatically. No manual SQL setup needed.

---

## 🚀 Deployment

This project is designed to be easily deployed on:

- **Railway** — Supports pgvector PostgreSQL natively; deploy backend & frontend as separate services
- **AWS EC2 / ECS** — Use Docker Compose directly on a VM
- **Render** — Deploy FastAPI and Streamlit as web services

For production, replace hardcoded DB credentials with environment variables and use a managed PostgreSQL service with pgvector support.

---

## 📌 Environment Variables

| Variable | Description |
|----------|-------------|
| `GOOGLE_API_KEY` | Your Google AI Studio / Gemini API key |

---

## 🤝 Use Cases

- 📋 **HR Policy Bot** — Let employees query company handbooks
- 🏥 **Medical Document Assistant** — Query clinical guidelines or reports
- 📦 **Product Manual Bot** — Answer customer questions from product docs
- ⚖️ **Legal Document Search** — Navigate contracts and legal filings
- 📊 **Business Report Analyst** — Ask questions about financial reports

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## 👤 Author

**[Your Name]**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Upwork / Fiverr: [Your Profile Link]

---

> ⭐ If you find this project useful, please give it a star!
