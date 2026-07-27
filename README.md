# SmartAssist AI — Full-Stack Conversational Chatbot

A full-stack AI chatbot platform built with Django REST Framework and React.js, powered by the Groq API (Meta Llama 3). Includes token-based authentication, persistent chat history, and a fully containerized Docker setup.

---


## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.x + Django REST Framework |
| Frontend | React.js 18 + Vite |
| AI Model | Meta Llama 3 via Groq Cloud API |
| Database | SQLite (via Django ORM) |
| Auth | Token-based authentication (DRF) |
| Deployment | Docker + Docker Compose |

---

## Features

- Real-time chat interface with streaming AI responses
- Token-based user authentication (register, login, logout)
- Persistent chat history stored per user session
- CORS-configured Django backend acting as a secure API proxy to Groq
- Fully containerized — runs with a single Docker Compose command

---

## System Flow

```
User Input (React)
    → Axios POST /api/chat/
        → Django validates auth token
            → Groq API (Llama 3) generates response
                → Saved to SQLite
                    → Response returned to frontend
```

---
## 🔗 Live API
Base URL: https://web-production-e7d7b.up.railway.app

| Endpoint | Method |
|---|---|
| /api/chat/ | POST |
| /api/auth/login/ | POST |
| /api/auth/register/ | POST |

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker Desktop (for containerized setup)
- Groq API key — get one free at [console.groq.com](https://console.groq.com)

---

### Option A: Run with Docker (Recommended)

```bash
git clone https://github.com/FAISALREHMAN-AI/smartassist-ai.git
cd smartassist-ai
```

Create a `.env` file in the `backend/` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Then start everything:

```bash
docker-compose up --build
```

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000/api/`

---

### Option B: Run Locally (Without Docker)

#### Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate        # Windows
source .venv/bin/activate       # macOS/Linux

pip install django djangorestframework django-cors-headers openai python-dotenv

python manage.py migrate
python manage.py runserver
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Environment Variables

Create `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
DEBUG=True
```

---

## Project Structure

```
smartassist-ai/
├── backend/
│   ├── chat/               # Chat API views and models
│   ├── users/              # Auth endpoints
│   ├── smartassist/        # Django settings and URLs
│   ├── manage.py
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/     # Chat UI components
│   │   └── pages/          # Login, Register, Chat pages
│   └── vite.config.js
└── docker-compose.yml
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login and get token |
| POST | `/api/chat/` | Send message, get AI response |
| GET | `/api/chat/history/` | Fetch user chat history |

---

## Built By 

**Faisal Rehman** — AI Developer & Full-Stack Engineer
[LinkedIn](https://linkedin.com/in/faisal-rehman-ai) · [GitHub](https://github.com/FAISALREHMAN-AI) · [Portfolio](https://faisal-rehman.lovable.app)
