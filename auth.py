"""
auth.py - Simple session-based authentication module.

Users: admin / admin123 and user1 / user123
No external auth library required - uses bcrypt for password hashing.
"""

import bcrypt
import streamlit as st

# ---------------------------------------------------------------------------
# User store — passwords are bcrypt-hashed at import time
# ---------------------------------------------------------------------------
_RAW_USERS = {
    "admin":  {"password": "admin123", "name": "Admin User"},
    "user1":  {"password": "user123",  "name": "User One"},
}

USERS = {
    username: {
        "name": data["name"],
        "hashed_pw": bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()),
    }
    for username, data in _RAW_USERS.items()
}


def _check_password(username: str, password: str) -> bool:
    """Return True if username exists and password matches the stored hash."""
    user = USERS.get(username)
    if not user:
        return False
    return bcrypt.checkpw(password.encode(), user["hashed_pw"])


def show_login_page():
    """
    Renders the login form. Sets st.session_state.logged_in,
    st.session_state.username, and st.session_state.name on success.
    Calls st.stop() if the user is not authenticated.
    """
    st.title("📄 RAG Chat PDF")
    st.subheader("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if _check_password(username.strip(), password):
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.session_state.name = USERS[username.strip()]["name"]
            st.rerun()
        else:
            st.error("❌ Incorrect username or password. Please try again.")

    st.stop()


def logout():
    """Clear session state and rerun to return to the login page."""
    for key in ["logged_in", "username", "name",
                "vectorstore", "chat_history", "pdf_name"]:
        st.session_state.pop(key, None)
    st.rerun()


def require_auth():
    """
    Call at the top of every page. Shows login form and stops
    execution if the user is not authenticated.
    """
    if not st.session_state.get("logged_in"):
        show_login_page()  # always ends with st.stop()
