# SmartAssist AI - Full-Stack Conversational Chatbot Platform

SmartAssist AI is an enterprise-grade, full-stack conversational application engineered to deliver seamless real-time interactions over a highly scalable infrastructure. The intelligence layer is backed by the ultra-fast **Groq AI Gateway (Meta Llama 3 Architecture)**, seamlessly bound to a robust Django REST Framework backend proxy and a highly reactive React.js frontend interface.

## ⚙️ Technical Architecture Stack

- **Backend Engineering:** Django 6.x & Django REST Framework (DRF)
- **Frontend Ecosystem:** React.js (v18+) powered by Vite Framework
- **AI Compilation Core:** Groq Cloud API SDK via Abstracted OpenAI Protocol
- **Database Model:** Local SQLite relational instance managed via Django ORM
- **Security & Session Layer:** Django Stateless Token-Based Cross-Origin Authentication
- **Virtualization & Deployment:** Multi-container Docker & Docker Compose Orchestration

## 🏛️ System Data Flow Pipeline

1. **Ingress Payload Request:** The React virtual DOM captures user inputs and securely dispatches an asynchronous JSON payload to the Django REST server via Axios at `/api/chat/`.
2. **Token Authentication Check:** The backend middleware interceptor parses the incoming HTTP headers to cross-verify cryptographic token signatures mapped to the database.
3. **API Processing Broker:** Once validated, the backend views instantiate a secure proxy client forwarding the payload context to the Meta Llama 3 computing layer on Groq Cloud.
4. **Relational Persistence Layer:** Upon receiving a successful compilation stream, the interaction record status updates asynchronously inside the local SQLite schema.
5. **Egress Rendering:** The compiled response structure resolves back through the API endpoints, updating state parameters instantly within the browser viewport.

---

## 🚀 Installation & Execution Workflow

### Prerequisites
Ensure your operating system is equipped with Python 3.11+, Node.js 18+, and Docker Desktop before setting up the operational environments.

### Deployment Method A: Standard Shell Terminal Execution

#### 1. Backend Microservice Deployment
```bash
# Navigate to the backend directory path
cd backend

# Initialize and activate isolated virtual package layer
python -m venv .venv
.\.venv\Scripts\activate

# Install essential dependencies
pip install django djangorestframework django-cors-headers openai python-dotenv

# Synchronize core database migrations
python manage.py migrate

# Initialize local development proxy gateway
python manage.py runserver