# RAG Chat PDF

A Streamlit-based web application that lets authenticated users upload PDF documents and ask natural-language questions about their content using Retrieval-Augmented Generation (RAG) powered by Google Gemini.

---

## Features

- **PDF Upload & Parsing** — Extracts text from uploaded PDFs using PyPDF2.
- **Vector Search** — Chunks text and stores embeddings in a local FAISS index for fast similarity search.
- **Google Gemini LLM** — Uses `gemini-2.5-flash` to generate grounded answers from retrieved context.
- **Google Generative AI Embeddings** — Uses `gemini-embedding-001` to embed text chunks.
- **Authentication** — Simple username/password login with bcrypt-hashed passwords.
- **Persistent Index** — FAISS index is saved to disk (`./faiss_index`) and survives restarts.
- **Docker Support** — Includes a ready-to-use Dockerfile.

---

## Project Structure

```
RAG_PDF/
├── app.py              # Main Streamlit application
├── auth.py             # Login / logout / session management
├── rag.py              # PDF extraction, vector store, RAG chain
├── config.yaml         # User credentials (bcrypt hashed)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container definition
└── faiss_index/        # Persisted FAISS vector index (auto-created)
```

---

## Prerequisites

- Python 3.11+
- A **Google AI API key** with access to Gemini models ([Get one here](https://aistudio.google.com/app/apikey))

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd RAG_PDF
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Running with Docker

### Build the image

```bash
docker build -t rag-chat-pdf .
```

### Run the container

```bash
docker run -p 8501:8501 \
  -e GOOGLE_API_KEY=your_google_api_key_here \
  -v $(pwd)/faiss_index:/app/faiss_index \
  rag-chat-pdf
```

Access the app at `http://localhost:8501`.

---

## Default Users

| Username | Password  | Role       |
|----------|-----------|------------|
| `admin`  | `admin123`| Admin User |
| `user1`  | `user123` | User One   |

> **Note:** Passwords are hashed with bcrypt at runtime. To add or change users, update `auth.py` (`_RAW_USERS`) or the hashed entries in `config.yaml`.

---

## How It Works

```
PDF Upload
    │
    ▼
Text Extraction (PyPDF2)
    │
    ▼
Text Chunking (RecursiveCharacterTextSplitter, 1000 chars / 200 overlap)
    │
    ▼
Embedding Generation (gemini-embedding-001)
    │
    ▼
FAISS Vector Store (persisted locally)
    │
    ▼
User Question → Similarity Search (top-5 chunks)
    │
    ▼
Prompt + Context → Gemini 2.5 Flash → Answer
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `langchain` + `langchain-text-splitters` | RAG orchestration & chunking |
| `langchain-google-genai` | Gemini LLM & embeddings |
| `langchain-community` | FAISS vector store integration |
| `faiss-cpu` | Local vector similarity search |
| `pypdf2` | PDF text extraction |
| `python-dotenv` | Environment variable loading |
| `bcrypt` | Password hashing |
| `pyyaml` | YAML config parsing |

