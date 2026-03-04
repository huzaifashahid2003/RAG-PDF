# ── Base image ────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── Environment variables ──────────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ── Working directory ──────────────────────────────────────────────────────────
WORKDIR /app

# ── System dependencies (needed by faiss-cpu and bcrypt) ──────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ── Python dependencies ────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Application source ─────────────────────────────────────────────────────────
COPY app.py auth.py rag.py config.yaml ./

# ── FAISS index persistence directory ─────────────────────────────────────────
# Mount a volume here at runtime to persist the index across container restarts:
#   docker run -v $(pwd)/faiss_index:/app/faiss_index ...
RUN mkdir -p faiss_index

# ── Streamlit port ─────────────────────────────────────────────────────────────
EXPOSE 8501

# ── Healthcheck ────────────────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

# ── Entrypoint ─────────────────────────────────────────────────────────────────
ENTRYPOINT ["streamlit", "run", "app.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0", \
            "--server.headless=true"]
