<div align="center">

# 🚀 AI Sales Outreach Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.138-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.58-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-Enabled-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white" />
  <img src="https://img.shields.io/badge/Google_Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-DB-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
</p>

<p align="center">
  <strong>An intelligent, full-stack agentic application that automates B2B lead management and generates hyper-personalized outreach emails using Google Gemini AI — all from a beautiful, production-ready interface.</strong>
</p>

<br/>

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Setup](#local-setup)
  - [Docker Deployment](#docker-deployment)
- [Environment Variables](#-environment-variables)
- [API Endpoints](#-api-endpoints)
- [How It Works](#-how-it-works)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧠 Overview

The **AI Sales Outreach Agent** is a full-stack, AI-powered application designed to streamline B2B sales outreach. It combines a **FastAPI** backend, a **Streamlit** frontend, and **Google Gemini** (via LangChain/LangGraph) to help sales teams manage prospects and automatically craft personalized cold emails — reducing manual work from hours to seconds.

> Built for teams who want to scale personalized communication without scaling headcount.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 📋 **Lead Management** | Add, view, and manage prospects with name, email, and company info |
| 🤖 **AI Email Generation** | Generates context-aware, personalized outreach emails using Google Gemini |
| ✏️ **Human-in-the-Loop Editing** | Review and edit AI-generated emails before sending |
| 📤 **One-Click Email Sending** | Send finalized emails directly from the UI via SMTP |
| 🗄️ **Persistent Storage** | All leads stored in a PostgreSQL database |
| 🐳 **Dockerized** | Fully containerized — runs anywhere with a single command |
| 🎨 **Gradient UI** | Beautiful, modern purple-gradient Streamlit interface |

---

## 🛠 Tech Stack

### Frontend
- **[Streamlit](https://streamlit.io/)** — Interactive web UI with real-time state management
- Custom CSS gradient theming for a polished, professional look

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** — High-performance async REST API
- **[Uvicorn](https://www.uvicorn.org/)** — ASGI server for production-grade performance
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — ORM for database interactions
- **[Pydantic](https://docs.pydantic.dev/)** — Data validation and settings management

### AI / Agentic Layer
- **[Google Gemini](https://deepmind.google/technologies/gemini/)** — LLM for email generation
- **[LangChain](https://www.langchain.com/)** — LLM orchestration framework
- **[LangGraph](https://www.langchain.com/langgraph)** — Stateful agentic workflow management
- **[FAISS](https://faiss.ai/)** — Vector similarity search (for future RAG capabilities)
- **[DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/)** — Web search for lead enrichment

### Database & Infrastructure
- **[PostgreSQL](https://www.postgresql.org/)** — Relational database for lead persistence
- **[Docker](https://www.docker.com/)** — Containerization for consistent deployments
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** — Secure environment configuration

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Docker Container                    │
│                                                         │
│   ┌─────────────────┐        ┌─────────────────────┐   │
│   │  Streamlit UI   │        │   FastAPI Backend    │   │
│   │   (Port 8501)   │◄──────►│    (Port 8000)       │   │
│   │                 │  HTTP  │                     │   │
│   │  - Add Leads    │        │  - CRUD Endpoints    │   │
│   │  - View List    │        │  - AI Email Gen      │   │
│   │  - Edit Email   │        │  - Email Dispatch    │   │
│   │  - Send Email   │        │                     │   │
│   └─────────────────┘        └────────┬────────────┘   │
│                                       │                 │
│                          ┌────────────▼────────────┐   │
│                          │     LangChain/LangGraph  │   │
│                          │   AI Orchestration Layer │   │
│                          └────────────┬────────────┘   │
│                                       │                 │
│                    ┌──────────────────▼──────────────┐ │
│                    │        Google Gemini API         │ │
│                    │  (Personalized Email Generation) │ │
│                    └─────────────────────────────────┘ │
│                                                         │
│   ┌─────────────────────────────────────────────────┐  │
│   │           PostgreSQL Database                   │  │
│   │              (Lead Storage)                     │  │
│   └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
ai-sales-outreach-agent/
│
├── app/
│   └── main.py              # FastAPI app — routes, DB models, AI logic
│
├── app.py                   # Streamlit frontend — UI components & state
│
├── requirements.txt         # Python dependencies (pinned versions)
├── Dockerfile               # Multi-service container definition
├── .env.example             # Environment variable template (safe to commit)
├── .env                     # ⚠️  Local secrets — NEVER commit this
├── .gitignore               # Excludes .env and other sensitive files
│
└── README.md                # You are here 📍
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- [Python 3.11+](https://www.python.org/downloads/)
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [PostgreSQL](https://www.postgresql.org/download/) (if running locally without Docker)
- A [Google AI Studio](https://aistudio.google.com/) API Key
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords) enabled

---

### Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/Noomaann/ai-sales-outreach-agent.git
cd ai-sales-outreach-agent
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
# Edit .env and fill in your credentials
```

**5. Start PostgreSQL and create the database**
```sql
CREATE DATABASE lead_agent_db;
```

**6. Run the backend (FastAPI)**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**7. Run the frontend (Streamlit) in a new terminal**
```bash
streamlit run app.py --server.port 8501
```

**8. Open your browser**
```
Frontend:  http://localhost:8501
API Docs:  http://localhost:8000/docs
```

---

### Docker Deployment

The easiest way to run the entire stack with a single command:

**1. Build the Docker image**
```bash
docker build -t ai-sales-outreach-agent .
```

**2. Run the container**
```bash
docker run -d \
  --env-file .env \
  -p 8000:8000 \
  -p 8501:8501 \
  --add-host=host.docker.internal:host-gateway \
  ai-sales-outreach-agent
```

**3. Access the app**
```
Frontend:  http://localhost:8501
API Docs:  http://localhost:8000/docs
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root. **Never commit this file to version control.**

```env
# Database
DATABASE_URL=postgresql://postgres:your_password@localhost/lead_agent_db

# Google Gemini AI
GOOGLE_API_KEY=your_google_api_key_here

# Email Sender (Gmail with App Password)
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

You can use the `.env.example` template:

```env
# .env.example — safe to commit, no real values
DATABASE_URL=postgresql://user:password@host/dbname
GOOGLE_API_KEY=your_google_api_key
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

> 💡 For Gmail, generate an [App Password](https://myaccount.google.com/apppasswords) — your regular Gmail password will not work.

---

## 📡 API Endpoints

The FastAPI backend exposes the following REST endpoints:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/leads/` | Fetch all leads |
| `POST` | `/leads/` | Add a new lead |
| `POST` | `/leads/{id}/generate-email` | Generate personalized AI email |
| `POST` | `/leads/{id}/send-email` | Send email to the lead |

Full interactive API documentation available at `http://localhost:8000/docs` (Swagger UI).

---

## 🔍 How It Works

```
1. 📋 ADD LEAD
   User enters name, email, company → stored in PostgreSQL via FastAPI

2. 🤖 GENERATE EMAIL
   FastAPI calls LangChain + Google Gemini with lead context
   → AI crafts a personalized cold email

3. ✏️ REVIEW & EDIT
   Email appears in an editable text area in the UI
   → Human can refine the AI-generated content

4. 🚀 SEND EMAIL
   Finalized content sent to FastAPI
   → Backend dispatches email via SMTP (Gmail)
   → Lead is updated in the database
```

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

Please make sure your code follows the existing style and all tests pass before submitting.

---

## 🔒 Security Notes

- **Never** commit your `.env` file — add it to `.gitignore`
- Rotate API keys and passwords if they are ever accidentally exposed
- Use environment variables or a secrets manager in production
- Gmail App Passwords should be treated like regular passwords

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ using FastAPI, Streamlit, LangChain & Google Gemini**

*If you found this project helpful, please consider giving it a ⭐ on [ai-sales-outreach-agent](https://github.com/your-username/ai-sales-outreach-agent)*

</div>
