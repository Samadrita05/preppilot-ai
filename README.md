# 🚀 PrepPilot AI

PrepPilot AI is a full-stack AI-powered interview preparation platform that helps users practice technical interviews and receive intelligent feedback.

Built with FastAPI (backend), React + Vite (frontend), and integrated with Groq LLM API for AI-generated evaluation.

---

## 🌟 Features

- 🔐 User Authentication (JWT-based login/signup)
- 🤖 AI-generated interview questions
- 📝 Answer evaluation with AI feedback
- 📊 Performance scoring and report generation
- 📄 PDF report download
- 🧠 Sentiment analysis
- 📈 Interview completion tracking

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- Alembic (Database migrations)
- JWT Authentication
- Groq LLM API
- SQLite (local development)

### Frontend
- React (Vite)
- React Router
- Modern CSS
- Fetch API

### Deployment
- Backend: Render
- Frontend: Netlify

---

## 📂 Project Structure
preppilot-ai/
│
├── backend/
│ ├── routers/
│ ├── services/
│ ├── database/
│ ├── core/
│ └── main.py
│
└── prep-pilot-frontend/
├── src/
├── components/
├── pages/
└── App.jsx

---

## ⚙️ Local Setup

### 1️⃣ Clone Repository

git clone https://github.com/YOUR_USERNAME/preppilot-ai.git
cd preppilot-ai


---

### 2️⃣ Backend Setup

cd backend
python -m venv venv
venv\Scripts\activate # Windows
pip install -r requirements.txt


Create a `.env` file:

GROQ_API_KEY=your_api_key_here


Run server:

uvicorn main:app --reload


---

### 3️⃣ Frontend Setup

cd prep-pilot-frontend
npm install
npm run dev


---

## 🔐 Environment Variables

### Backend
GROQ_API_KEY=your_api_key


### Frontend
VITE_API_URL=http://127.0.0.1:8000


---

## 🌍 Live Demo

Frontend: (Add Netlify link after deployment)  
Backend API: (Add Render link after deployment)

---

## 📌 Future Improvements

- PostgreSQL for production
- Role-based access control
- Advanced analytics dashboard
- Interview history comparison
- Dark mode UI

---

## 👩‍💻 Author

Samadrita Hazra  
GitHub: https://github.com/Samadrita05

---

## 📄 License

This project is for educational and portfolio purposes.
