# 🚀 Backend & Frontend Separation + Automated Trading System

## 📌 Overview
This project is an automated stock trading system that separates the backend and frontend. It utilizes **Django Ninja** for the backend API, **Django Templates** for the frontend, and **Celery** for asynchronous tasks. The system fetches stock data via **Kiwoom REST API**, executes trades based on predefined strategies, and is containerized using **Docker & Docker Compose**.

## 📂 Project Structure
```
trading-with-kiwoom-api/
├── backend/        # Backend (Django Ninja API, Celery, Kiwoom API Integration)
│   ├── _core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── celery.py
│   │   ├── wsgi.py
│   ├── a_stocks/
│   │   ├── api.py  # Django Ninja API
│   │   ├── models.py
│   │   ├── views.py
│   ├── manage.py
│   ├── Dockerfile
│
├── frontend/       # Frontend (Django Templates, JavaScript Fetch API)
│   ├── templates/
│   │   ├── stocks/
│   │   │   ├── list.html
│   ├── static/
│   ├── views.py
│   ├── urls.py
│
├── docker-compose.yml
```

## 🛠️ Technologies Used
- **Backend:** Django Ninja, Django, Celery, Kiwoom REST API
- **Frontend:** Django Templates, JavaScript (Fetch API)
- **Database & Queues:** PostgreSQL, Redis
- **Containerization:** Docker, Docker Compose
- **Asynchronous Processing:** Celery
- **Web Server:** Uvicorn

## 🔧 Setup & Installation
- UV: Python package installer
### 1️⃣ Clone the repository
```bash
git clone https://github.com/bamjun/trading-with-kiwoom-api.git
cd trading-with-kiwoom-api
```

### 2️⃣ Setup Backend
```bash
cd backend
uv sync
# window
source .venv/scripts/activate
# linux
source .venv/bin/activate
python manage.py migrate
python manage.py runserver 8000
```

### 3️⃣ Setup Frontend
```bash
cd frontend
uv venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver 8001
```

### 4️⃣ Run with Docker Compose
```bash
docker-compose up --build
```

## 🚀 Features
- 📈 **Stock Data Fetching:** Fetch real-time stock data from Kiwoom REST API.
- 🏦 **Automated Trading:** Execute buy/sell strategies based on predefined rules.
- 🔄 **Celery Task Scheduling:** Run background jobs for data processing.
- 🌐 **Django Ninja API:** Provide fast and scalable RESTful API.
- 🎨 **Frontend with Django Templates:** Display real-time stock information dynamically.

## 📌 API Endpoints
### ✅ Stock Data API (Backend: Django Ninja)
- `GET /api/stocks/` → Fetch stock list
- `POST /api/trade/` → Execute trade order

## 📌 Frontend Page (Django Templates)
- `/stocks/list/` → Displays stock data dynamically using Fetch API

## ✅ Completion Criteria
- The **Django Ninja API** should be accessible at `http://localhost:8000/api/stocks/`
- The **frontend** should load data from the API at `http://localhost:8001/stocks/list/`
- Celery should be **connected to Redis** and run background tasks
- The **Docker containers** should start properly

## 📚 Documentation & References
- [Django Ninja Docs](https://django-ninja.rest-framework.com/)
- [Django Official Docs](https://docs.djangoproject.com/en/)
- [Celery Docs](https://docs.celeryq.dev/en/stable/)
- [Kiwoom REST API Guide](https://openapi.kiwoom.com/main/home)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [UV Docs](https://docs.astral.sh/uv/)
- [keys](https://www.notion.so/twika-1c28c2bbc2e080f9bdece247ab1ad693)