# SmartAssist AI - Full-Stack Conversational Chatbot

SmartAssist AI ek enterprise-grade, full-stack conversational platform hai jo users ko ek asynchronous real-time chat interface provide karta hai. Yeh application high-speed **Groq AI (Llama 3 Architecture)** engine se powered hai, jise backend pipeline par Django REST Framework aur client side par React.js + Vite ke sath tightly integrate kiya gaya hai.

## ⚙️ Technical Architecture Stack

- **Backend Framework:** Django 6.x & Django REST Framework (DRF)
- **Frontend Ecosystem:** React.js (v18+) & Vite Framework (Dark Mode Responsive UI)
- **AI Compilation Layer:** Groq Cloud API SDK via OpenAI Client Core
- **Database Architecture:** SQLite Instance managed through Django ORM
- **Security & Session Layer:** Django Token-Based Cross-Origin Authentication
- **Containerization:** Docker Framework & Docker Compose Engine

## 🏛️ System Data Flow Diagram

1. **Client Request:** React UI capture karta hai user ka message aur use Axios client ke zariye Django POST endpoint `/api/chat/` par push karta hai.
2. **Token Security:** Django middleware request header se authorization token cross-verify karta hai.
3. **AI Compilation:** Backend proxy client securely invoke karta hai Groq API gateway ko using Meta Llama-3 (8B) infrastructure.
4. **Data Relational Storage:** Success execution ke baad session array state save hoti hai relational local SQLite database mein.
5. **UI Rendering:** Output payload dynamic asynchronous state update ke zariye client application screen par display hota hai.

---

## 🚀 Local Installation & Execution Guide

### Prerequisite Setup
Aapke local machine par Python 3.11+, Node.js 18+, aur Docker Desktop configured hona chahiye.

### Setup Method A: Running via Native Terminal

#### 1. Backend Runtime Environment Setup
```bash
# Navigate to backend path
cd backend

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install required components
pip install django djangorestframework django-cors-headers openai python-dotenv

# Execute Database Migration
python manage.py migrate

# Initiate Local Web Server
python manage.py runserver