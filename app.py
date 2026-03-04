"""
app.py - Main Streamlit application for RAG PDF Chat.
"""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="RAG Chat PDF",
    page_icon="📄",
    layout="wide",
)

from auth import require_auth, logout
from rag import extract_text_from_pdf, create_vector_store, ask_question

# ── Auth gate: shows login form and stops if not logged in ───────────────────
require_auth()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📄 RAG Chat PDF")
    st.markdown(f"**{st.session_state.get('name', '')}**")
    st.caption(f"@{st.session_state.get('username', '')}")
    st.markdown("---")
    if st.button("Logout"):
        logout()


# ── Session state defaults ───────────────────────────────────────────────────
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

# ── Main content ─────────────────────────────────────────────────────────────
st.title("📄 RAG Chat PDF")
st.caption("Upload a PDF and ask questions about its content.")
st.markdown("---")

# ── PDF Upload ───────────────────────────────────────────────────────────────
st.subheader("Upload PDF")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    if st.session_state.pdf_name != uploaded_file.name:
        with st.spinner("Processing PDF..."):
            try:
                raw_text = extract_text_from_pdf(uploaded_file)
                if not raw_text.strip():
                    st.error("No text found in this PDF. It may be image-based.")
                    st.stop()
                vectorstore = create_vector_store(raw_text)
                st.session_state.vectorstore = vectorstore
                st.session_state.pdf_name = uploaded_file.name
                st.session_state.chat_history = []
                st.success(f"✅ **{uploaded_file.name}** processed. Ask your questions below.")
            except Exception as e:
                st.error(f"Error processing PDF: {e}")
                st.stop()
    else:
        st.info(f"📎 **{uploaded_file.name}** is already loaded.")

# ── Q&A ──────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Ask a Question")

if st.session_state.vectorstore is None:
    st.warning("Upload a PDF above to get started.")
else:
    user_question = st.text_input(
        "Your question:",
        placeholder="e.g. What is the main topic of this document?",
        key="question_input",
    )
    if st.button("Ask", type="primary"):
        if user_question.strip():
            with st.spinner("Thinking..."):
                try:
                    answer = ask_question(st.session_state.vectorstore, user_question)
                    st.session_state.chat_history.insert(
                        0, {"question": user_question, "answer": answer}
                    )
                except Exception as e:
                    st.error(f"Error generating answer: {e}")
        else:
            st.warning("Please enter a question.")

# ── Chat History ─────────────────────────────────────────────────────────────
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("Chat History")
    for idx, entry in enumerate(st.session_state.chat_history):
        st.markdown(f"**Q{idx + 1}: {entry['question']}**")
        st.info(entry["answer"])
    if st.button("Clear History"):
        st.session_state.chat_history = []
        st.rerun()
