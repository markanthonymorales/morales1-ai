# Morales1 AI Project

This project sets up a self-hosted AI system using `gemma3:4b-it-qat` as the base model with RAG (Retrieval-Augmented Generation) and MCP (Modular Cloud Protection) tools.

---

## 🚀 Quick Start

### Prerequisites:
- Docker & Docker Compose installed
- At least 8-12GB of RAM recommended

### Run Everything
```bash
docker-compose up --build
```
> This will:
> - Build and run the Ollama model `morales1`
> - Start FastAPI backend with RAG + MCP Tools
> - Launch a minimal frontend chat UI


---

## 📁 Folder Structure
```
Morales1/
├── backend/
│   ├── Dockerfile
│   └── app/
│       ├── main.py
│       ├── rag_engine.py
│       ├── ingest.py
│       ├── mcp_tools.py
│       └── util.py
├── frontend/
│   ├── app.js
│   ├── style.css
│   └── public/
│       └── index.html
├── ollama/
│   └── Modelfile
├── requirements.txt
├── docker-compose.yml
└── .gitignore
```

---

## 🧠 Features
- ✅ **Custom AI model (morales1)** using Gemma 3B-IT
- ✅ **Vector search** using Qdrant for RAG
- ✅ **FastAPI backend** with endpoints for chat + knowledge ingestion
- ✅ **MCP tools** to simulate Cloudflare and DNS checks
- ✅ **Minimal frontend** with JS fetch-based chat

---

## 🛠 Endpoints

- `POST /chat`: Send a user question and get a response
- `POST /ingest`: Send documents to index into Qdrant

---

## 🧪 Example MCP Commands
Ask in chat:
- `run mcp:cloudflare example.com`
- `run mcp:dnscheck example.com`

---

## 🔐 .gitignore
```
__pycache__/
.env
*.log
.vscode/
.idea/
```

---

## ✨ Future Additions
- [ ] File uploads for ingestion
- [ ] Full MCP diagnostic pipelines
- [ ] Enhanced frontend with chat history

---

## 📬 Maintainer
Mark Anthony Morales — powered by Morales1