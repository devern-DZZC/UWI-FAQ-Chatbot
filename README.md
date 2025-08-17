# 🔍 AskUWI: Retrieval-Augmented Question Answering App

A full-stack AI-powered application that lets students ask natural language questions and receive accurate, context-aware answers from official UWI Faculty and FAQ documents — using RAG (Retrieval-Augmented Generation), OpenAI GPT models, and modern web technologies.

Live Demo: https://ask-uwi.azurewebsites.net  
Demo Video: https://www.youtube.com/watch?v=bC1Jhql9CH4

---

## ✨ Features

- ⚡ **FastAPI + LangChain RAG backend**: Uses vector search (FAISS) and OpenAI’s GPT-4/3.5 for contextual question answering
- 🌐 **Modern React frontend**: Clean, minimal UI built with Vite + React + Tailwind CSS
- 🔗 **CORS-ready**: Frontend and backend communicate securely across localhost/dev environments

---

## 🧠 Tech Stack

| Layer     | Technology                  |
|----------|------------------------------|
| Frontend | React + Vite + Tailwind CSS  |
| Backend  | FastAPI + LangChain + FAISS  |
| AI Model | OpenAI GPT-4 / GPT-3.5       |
| Vector DB| FAISS (in-memory)            |
| Storage  | SQLite (temporary metadata)  |

---

# 🚀 Getting Started

## 1. Clone the Repo

```bash
git clone https://github.com/devern-DZZC/UWI-FAQ-Chatbot.git
cd UWI-FAQ-Chatbot
```

2. Backend Setup (FastAPI)
```bash
cd app
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY=your_key_here  # On Windows: set OPENAI_API_KEY=your_key_here

# Run the backend
uvicorn main:app --reload

```

3. Frontend Setup (React)
```bash
cd frontend
npm install
npm run dev
```

✅ Make sure your backend is running at http://localhost:8000


