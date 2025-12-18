# 📚 RAG Q&A Chatbot (FastAPI + LangChain + FAISS + Gemini)

## 📌 Description du projet
Ce projet est une application de Question–Réponse basée sur le principe de RAG (Retrieval-Augmented Generation).
Il permet de poser des questions en langage naturel sur le document Schatzinsel_E.pdf.

## 🧠 Architecture
User → FastAPI → FAISS Retriever → Gemini LLM → Answer + Sources

## 🛠️ Technologies
- Python 3.11
- FastAPI
- LangChain
- FAISS
- Sentence-Transformers
- Google Gemini
- React (Frontend)

## 📂 Structure
.
├── backend/
│   ├── app/
│   │   ├── data/
│   │   │   ├── documents/
│   │   ├── main.py
│   │   ├── api.py
│   │   ├── config.py
│   │   ├── rag/
│   │   │   ├── ingest.py
│   │   │   ├── retriever.py
│   │   │   └── generator.py
│   ├── vectorstore/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
|   |   ├──Chat.module.css
|   |   ├──globals.css
|   |   ├──layout.tsx
│   │   └── page.tsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── docker.sh
└── README.md

## ⚙️ Installation
```bash
git clone <repo>
cd Coding Challenge
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
```

## 🔑 Variables d’environnement
```bash
setx GOOGLE_API_KEY "your_api_key"
```

## 📥 Ingestion
```bash
cd backend
python -m app.rag.ingest
```

## 🧪 Test RAG sans API
```bash
python test_rag.py
```

## 🚀 Lancer l’API
```bash
uvicorn app.main:app --reload
```
Swagger: http://127.0.0.1:8000/docs

## 🎨 Frontend
```bash
cd frontend
npm install
npm start
```

## 👤 Auteur
Souhail Bouri
