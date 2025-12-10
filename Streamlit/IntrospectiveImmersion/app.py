# ═══════════════════════════════════════════════════════════════════════
#  app.py - MAIN ENTRY POINT (Handles Login and Page Configuration)
# ═══════════════════════════════════════════════════════════════════════

import streamlit as st
import hashlib

# ─────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION (Must be first)
# ─────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Introspective Immersion",
    page_icon="✨",
    layout="centered"
)

# ─────────────────────────────────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────────────────────────────────

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'users' not in st.session_state:
    st.session_state.users = {} 

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'quiz_results' not in st.session_state:
    st.session_state.quiz_results = {}


# ─────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS (Kept for Login/Registration)
# ─────────────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Simple password hashing."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username: str, password: str) -> bool:
    """Verify credentials."""
    hashed_pass = hash_password(password)
    return st.session_state.users.get(username) == hashed_pass


def register_user(username: str, password: str) -> tuple[bool, str]:
    """Register a new user."""
    if username in st.session_state.users:
        return (False, "Username already taken")
    
    if len(password) < 6:
        return (False, "Password must be at least 6 characters long")
    
    st.session_state.users[username] = hash_password(password)
    st.session_state.quiz_results[username] = {} 
    return (True, "Registration successful! Please login.")


def show_login_form():
    """Display the login form."""
    st.subheader("Authentication")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Access Portal")
        
        if submitted:
            if check_credentials(username, password):
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.rerun()
            else:
                st.error("Invalid Username or Password. Denied access.")


def show_registration_form():
    """Display the registration form."""
    st.subheader("Registration")
    
    with st.form("registration_form"):
        new_username = st.text_input("Desired Username")
        new_password = st.text_input("Secure Password (min 6 chars)", type="password")
        submitted = st.form_submit_button("Register")
        
        if submitted:
            success, message = register_user(new_username, new_password)
            if success:
                st.success(message)
                st.session_state.login_tab_selected = True 
            else:
                st.error(message)


# ─────────────────────────────────────────────────────────────────────────
# MAIN APPLICATION LOGIC
# ─────────────────────────────────────────────────────────────────────────

def main():
    st.title("Introspective Immersion")
    st.caption("*Find your true self*")
    
    if st.session_state.get('logged_in', False):
        # Redirect to the main page (Archetype Quiz) by default
        st.info("Authentication successful. Please select a page from the sidebar.")
    else:
        # Show Login/Registration
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            show_login_form()
        with tab2:
            show_registration_form()
            
        if 'login_tab_selected' in st.session_state:
            del st.session_state.login_tab_selected


if __name__ == "__main__":
    main()