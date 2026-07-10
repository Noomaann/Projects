# 🎫 AI Customer Support Ticket System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![HuggingFace](https://img.shields.io/badge/🤗_HuggingFace-Transformers-FFD21E?style=for-the-badge)

**An intelligent, AI-powered customer support ticket management system with real-time NLP analysis, automatic classification, and AI-generated reply drafts.**

[Features](#-features) · [Tech Stack](#-tech-stack) · [Project Structure](#-project-structure) · [Setup](#-setup--installation) · [API Docs](#-api-endpoints) · [Screenshots](#-screenshots)

</div>

---

## ✨ Features

- 🏷️ **Auto-Classification** — Automatically categorizes tickets into Refund, Complaint, Delivery, Technical Issue, Pricing, Feedback, and General Inquiry
- 💬 **Sentiment Analysis** — Detects whether the customer's tone is Positive, Negative, or Neutral
- 🚨 **Priority Scoring** — Assigns High / Medium / Low priority based on sentiment and category
- 🤖 **AI Reply Drafts** — Generates a professional reply draft using Google's Flan-T5 model
- 📊 **Live Dashboard** — Beautiful Streamlit dashboard with real-time charts and metrics
- 🐳 **Dockerized** — Fully containerized with Docker Compose for easy deployment
- 🗄️ **Persistent Storage** — All tickets stored in PostgreSQL database

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend API** | FastAPI + Uvicorn |
| **Frontend Dashboard** | Streamlit + Plotly |
| **Database** | PostgreSQL + SQLAlchemy |
| **NLP Models** | HuggingFace Transformers |
| **Sentiment Analysis** | `distilbert-base-uncased-finetuned-sst-2-english` |
| **Classification** | `facebook/bart-large-mnli` (Zero-Shot) |
| **Reply Generation** | `google/flan-t5-base` |
| **Containerization** | Docker + Docker Compose |

---

## 📁 Project Structure

```
ai-support-ticket-system/
│
├── backend/
│   ├── Dockerfile          # Backend container config
│   ├── main.py             # FastAPI app & route handlers
│   ├── models.py           # SQLAlchemy database models
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── database.py         # DB connection & session management
│   ├── nlp_utils.py        # HuggingFace NLP pipeline logic
│   └── requirements.txt    # Backend Python dependencies
│
├── frontend/
│   ├── Dockerfile          # Frontend container config
│   ├── app.py              # Streamlit dashboard UI
│   └── requirements.txt    # Frontend Python dependencies
│
├── docker-compose.yml      # Multi-container orchestration
├── .env.example            # Sample environment variables
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [PostgreSQL](https://www.postgresql.org/download/) running locally (or via Docker)
- Git

---

### 🐳 Method 1: Run with Docker Compose (Recommended)

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ai-support-ticket-system.git
cd ai-support-ticket-system
```

**2. Set up environment variables**
```bash
cp .env.example .env
```
Open `.env` and fill in your database credentials:
```env
DATABASE_URL=postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@host.docker.internal:5432/ticket_db
```

**3. Create the database** (in PostgreSQL)
```sql
CREATE DATABASE ticket_db;
```

**4. Build and run all services**
```bash
docker-compose up --build
```

**5. Access the apps**

| Service | URL |
|---------|-----|
| 🖥️ Streamlit Dashboard | http://localhost:8505 |
| ⚡ FastAPI Backend | http://localhost:8080 |
| 📄 API Swagger Docs | http://localhost:8080/docs |

> **Note:** The first startup may take a few minutes as Docker downloads the HuggingFace NLP models (~1–2 GB).

---

### 💻 Method 2: Run Locally (Without Docker)

**1. Set up the Backend**
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` folder:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ticket_db
```

Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

**2. Set up the Frontend** (in a new terminal)
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py --server.port 8505
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root based on `.env.example`:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |

---

## 📡 API Endpoints

### Base URL: `http://localhost:8080`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/tickets/` | Submit a new support ticket |
| `GET` | `/tickets/all` | Fetch all tickets (newest first) |

### Example: Submit a Ticket

```bash
curl -X POST "http://localhost:8080/tickets/" \
  -H "Content-Type: application/json" \
  -d '{"customer_message": "I have not received my refund yet. It has been 7 days!"}'
```

**Response:**
```json
{
  "id": 1,
  "customer_message": "I have not received my refund yet. It has been 7 days!",
  "category": "Refund",
  "sentiment": "Negative",
  "priority_score": "High",
  "ai_reply_draft": "Thank you for reaching out. We sincerely apologize for the delay and will resolve your refund immediately."
}
```

Full interactive API documentation available at: **http://localhost:8080/docs**

---

## 📸 Screenshots

> _Add screenshots of your running dashboard here._

**Dashboard Overview**
<!-- ![Dashboard](screenshots/dashboard.png) -->

**Ticket Detail with AI Reply**
<!-- ![Ticket Detail](screenshots/ticket-detail.png) -->

---

## 🤖 NLP Models Used

| Task | Model | Source |
|------|-------|--------|
| Sentiment Analysis | `distilbert-base-uncased-finetuned-sst-2-english` | HuggingFace |
| Zero-Shot Classification | `facebook/bart-large-mnli` | Meta AI |
| Reply Generation | `google/flan-t5-base` | Google |

> Models are downloaded automatically on first run via HuggingFace's model hub.

---

## 🚀 How It Works

```
Customer Message
      │
      ▼
 FastAPI Backend
      │
      ├──► Sentiment Analysis  ──► Positive / Negative / Neutral
      │
      ├──► Zero-Shot Classification ──► Category (Refund, Complaint, etc.)
      │
      ├──► Priority Scoring Logic ──► High / Medium / Low
      │
      └──► Flan-T5 Reply Generator ──► AI Draft Reply
            │
            ▼
      Saved to PostgreSQL
            │
            ▼
   Streamlit Dashboard
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
Made with ❤️ using FastAPI, Streamlit, and HuggingFace Transformers
</div>
