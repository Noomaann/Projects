# 📊 AI Data Analyst Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
</p>

<p align="center">
  <b>Upload any CSV → Ask questions in plain English → Get instant AI-powered insights & charts</b>
</p>

---

## 🌟 What Is This?

**AI Data Analyst Agent** is a full-stack intelligent data analysis tool that lets you upload any CSV file and immediately start asking natural language questions about your data — no SQL knowledge required. Powered by **Google Gemini 2.5 Flash** and **LangChain**, the AI automatically generates and executes SQL queries under the hood, returning answers, visualizations, and executive reports.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📤 **CSV Upload** | Upload any CSV file and it's instantly stored in PostgreSQL |
| 💬 **Natural Language Q&A** | Ask questions like *"What is the average area_mean?"* and get instant answers |
| 📊 **AI Chart Generation** | Request charts like *"Show a bar chart of diagnosis vs area_mean"* |
| 📄 **Executive Report** | One-click AI-generated business summary with downloadable TXT export |
| 🐳 **Fully Dockerized** | Spin up the entire stack with a single `docker-compose up` command |

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                             │
│              Streamlit  +  Plotly  +  Requests              │
├─────────────────────────────────────────────────────────────┤
│                         Backend                             │
│         FastAPI  +  LangChain  +  Google Gemini 2.5         │
├─────────────────────────────────────────────────────────────┤
│                        Database                             │
│            PostgreSQL  +  SQLAlchemy  +  psycopg2           │
├─────────────────────────────────────────────────────────────┤
│                     Infrastructure                          │
│                  Docker  +  Docker Compose                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
ai-data-analyst/
│
├── backend/
│   ├── __init__.py          # Makes backend a Python package
│   ├── main.py              # FastAPI app & API endpoints
│   ├── agent.py             # LangChain + Gemini AI logic
│   ├── database.py          # SQLAlchemy engine & session setup
│   └── .env                 # 🔒 Secret keys (DO NOT commit to Git!)
│
├── frontend/
│   └── app.py               # Streamlit UI
│
├── Dockerfile               # Docker image build instructions
├── docker-compose.yml       # Multi-service orchestration
├── requirements.txt         # Python dependencies
├── .env.example             # Template for environment variables
├── .gitignore               # Git ignored files
└── README.md                # You are here!
```

---

## ⚙️ Setup & Installation

### Prerequisites

Make sure you have the following installed:
- [Docker](https://www.docker.com/get-started) & [Docker Compose](https://docs.docker.com/compose/)
- A [Google AI Studio](https://aistudio.google.com/) API key (free)
- A running **PostgreSQL** instance (or use a cloud DB like Supabase / Neon)

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-data-analyst.git
cd ai-data-analyst
```

### 2. Set Up Environment Variables

Copy the example env file and fill in your credentials:

```bash
cp .env.example backend/.env
```

Then open `backend/.env` and add your values:

```env
GOOGLE_API_KEY="your_google_gemini_api_key_here"
DATABASE_URL="postgresql://username:password@host:5432/ai_analyst_db"
```

> 💡 **Get your Gemini API key** for free at [Google AI Studio](https://aistudio.google.com/app/apikey)

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

That's it! The services will start automatically:

| Service | URL |
|---|---|
| 🎨 Frontend (Streamlit) | http://localhost:8501 |
| ⚡ Backend (FastAPI) | http://localhost:8000 |
| 📖 API Docs (Swagger) | http://localhost:8000/docs |

---

## 🚀 How to Use

1. **Open** `http://localhost:8501` in your browser
2. **Upload** a CSV file using the sidebar uploader
3. **Click** `🚀 Upload & Connect to DB`
4. **Ask** anything in the text box:
   - *"How many rows are in the dataset?"*
   - *"What is the maximum radius_mean?"*
   - *"Show a bar chart of diagnosis counts"*
5. Click **✨ Analyze Text** for a written answer or **📊 Generate Chart** for a visualization
6. Click **📑 Generate & Export Report** for a full executive summary

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/upload-csv/` | Upload a CSV file to the database |
| `POST` | `/ask/` | Ask a natural language question |
| `POST` | `/generate-chart/` | Generate chart data from a question |
| `GET` | `/generate-summary/` | Generate an executive business report |

> Full interactive API documentation available at `http://localhost:8000/docs`

---

## 🔒 Environment Variables

| Variable | Description | Example |
|---|---|---|
| `GOOGLE_API_KEY` | Google Gemini API key from AI Studio | `AIzaSy...` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/dbname` |

---

## 🧠 How It Works

```
User Question (Natural Language)
         ↓
    LangChain Prompt
         ↓
  Google Gemini 2.5 Flash
  (Reads DB Schema → Generates SQL)
         ↓
   SQLAlchemy executes SQL
   on PostgreSQL database
         ↓
  Result returned to FastAPI
         ↓
  Streamlit displays answer / chart
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ using FastAPI, Streamlit & Google Gemini
</p>
