# ═══════════════════════════════════════════════════════════════════════
#  CITIZEN WELLNESS PORTAL™
#  AlgoCratic Futures - ORANGE Clearance Authorization
# ═══════════════════════════════════════════════════════════════════════
#
#  Your mission: Build a login/registration system with dashboard
#  using Streamlit and AI-assisted learning.
#
#  Run with: streamlit run 06-starter-app.py
#
# ═══════════════════════════════════════════════════════════════════════

import streamlit as st
import hashlib

# ─────────────────────────────────────────────────────────────────────────
# QUIZ DATA STRUCTURES
# ─────────────────────────────────────────────────────────────────────────

# Maps characters to their underlying archetype
CHARACTERS = {
    # Star Wars
    "Luke Skywalker": "Hero",
    "Darth Vader": "Villain",
    "Princess Leia Organa": "Innocent",
    "Han Solo": "Anti-Hero",
    "Obi-Wan Kenobi": "Mentor",
    
    # Star Trek
    "James T. Kirk": "Hero",
    "Spock": "Mentor",
    "Nyota Uhura": "Innocent",
    "Leonard “Bones” McCoy": "Anti-Hero",
    "Montgomery Scott": "Villain",
    
    # Cyberpunk
    "V": "Hero",
    "Johnny Silverhand": "Anti-Hero",
    "Judy Alvarez": "Innocent",
    "Panam Palmer": "Mentor",
    "Jackie Welles": "Villain",
    
    # Harry Potter
    "Harry Potter": "Hero",
    "Hermione Granger": "Innocent",
    "Ron Weasley": "Villain",
    "Albus Dumbledore": "Mentor",
    "Severus Snape": "Anti-Hero",
    
    # BG3 (Baldur's Gate 3)
    "Karlach": "Innocent",
    "Astarion": "Anti-Hero",
    "Shadowheart": "Hero",
    "Gale": "Mentor",
    "Lae’zel": "Villain",
    
    # Naruto
    "Naruto Uzumaki": "Hero",
    "Sasuke Uchiha": "Anti-Hero",
    "Sakura Haruno": "Innocent",
    "Kakashi Hatake": "Mentor",
    "Itachi Uchiha": "Villain",
    
    # JJK (Jujutsu Kaisen)
    "Yuji Itadori": "Hero",
    "Megumi Fushiguro": "Innocent",
    "Nobara Kugisaki": "Anti-Hero",
    "Satoru Gojo": "Mentor",
    "Suguru Geto": "Villain",
}

# Questions, with character lists for radio buttons
ARCHETYPE_QUESTIONS = [
    {
        "id": 1,
        "question": "Which Star Wars character's moral compass do you trust the most?",
        "choices": ["Luke Skywalker", "Darth Vader", "Princess Leia Organa", "Han Solo", "Obi-Wan Kenobi"]
    },
    {
        "id": 2,
        "question": "Whose leadership style from Star Trek appeals to you?",
        "choices": ["James T. Kirk", "Spock", "Nyota Uhura", "Leonard “Bones” McCoy", "Montgomery Scott"]
    },
    {
        "id": 3,
        "question": "In the world of Cyberpunk, who would you choose as your main partner?",
        "choices": ["V", "Johnny Silverhand", "Judy Alvarez", "Panam Palmer", "Jackie Welles"]
    },
    {
        "id": 4,
        "question": "From the Harry Potter universe, whose perspective on magic/life do you share?",
        "choices": ["Harry Potter", "Hermione Granger", "Ron Weasley", "Albus Dumbledore", "Severus Snape"]
    },
    {
        "id": 5,
        "question": "Among the BG3 companions, who do you believe has the strongest inner resolve?",
        "choices": ["Karlach", "Astarion", "Shadowheart", "Gale", "Lae’zel"]
    },
    {
        "id": 6,
        "question": "If you were a Ninja, who would be your ideal sensei or rival from Naruto?",
        "choices": ["Naruto Uzumaki", "Sasuke Uchiha", "Sakura Haruno", "Kakashi Hatake", "Itachi Uchiha"]
    },
    {
        "id": 7,
        "question": "In the world of JJK, which character would you most likely follow into a fight?",
        "choices": ["Yuji Itadori", "Megumi Fushiguro", "Nobara Kugisaki", "Satoru Gojo", "Suguru Geto"]
    },
]

# ─────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Citizen Wellness Portal™",
    page_icon="🏛️",
    layout="centered"
)

# ─────────────────────────────────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────────────────────────────────

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'users' not in st.session_state:
    # {username: password_hash} - Use real hashing in production!
    st.session_state.users = {} 

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'quiz_results' not in st.session_state:
    # Stores results for the current user: {username: {'Hero': 3, 'Villain': 2, ...}}
    st.session_state.quiz_results = {}


# ─────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Simple password hashing."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username: str, password: str) -> bool:
    """
    Verify if username and password match a registered user.
    """
    hashed_pass = hash_password(password)
    return st.session_state.users.get(username) == hashed_pass


def register_user(username: str, password: str) -> tuple[bool, str]:
    """
    Register a new user.
    """
    if username in st.session_state.users:
        return (False, "Username already taken")
    
    if len(password) < 6:
        return (False, "Password must be at least 6 characters long")
    
    st.session_state.users[username] = hash_password(password)
    # Initialize their quiz results to empty
    st.session_state.quiz_results[username] = {} 
    return (True, "Registration successful! Please login.")

def calculate_archetype(results: dict[str, int]) -> tuple[str, int]:
    """
    Calculates the user's primary archetype from the quiz results.
    """
    if not results or all(v == 0 for v in results.values()):
        return ("Citizen Undetermined", 0)
    
    # Find the archetype with the highest count
    primary_archetype = max(results, key=results.get)
    max_score = results[primary_archetype]
    
    # Check for ties
    tied_archetypes = [k for k, v in results.items() if v == max_score]
    if len(tied_archetypes) > 1:
        # Report the tie
        return (f"Tied ({' & '.join(tied_archetypes)})", max_score)
        
    return (primary_archetype, max_score)


# ─────────────────────────────────────────────────────────────────────────
# VIEW FUNCTIONS (Forms and Dashboard)
# ─────────────────────────────────────────────────────────────────────────

def show_login_form():
    """
    Display the login form.
    """
    st.subheader("🔐 Citizen Authentication")
    
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
    """
    Display the registration form.
    """
    st.subheader("📝 New Citizen Registration")
    
    with st.form("registration_form"):
        new_username = st.text_input("Desired Username")
        new_password = st.text_input("Secure Password (min 6 chars)", type="password")
        submitted = st.form_submit_button("Register")
        
        if submitted:
            success, message = register_user(new_username, new_password)
            if success:
                st.success(message)
                # After successful registration, show the login tab automatically
                st.session_state.login_tab_selected = True 
            else:
                st.error(message)


def show_quiz():
    """
    Display the character preference quiz and process submissions.
    """
    st.header("✨ Archetype Profiling")
    st.markdown("### Select your favorite character from each set.")
    
    current_user = st.session_state.current_user
    
    # Use a Streamlit form to process all questions at once
    with st.form("archetype_quiz_form"):
        quiz_submission = {}
        
        for q_data in ARCHETYPE_QUESTIONS:
            st.markdown(f"**Q{q_data['id']}.** *{q_data['question']}*")
            # Create a unique key for each radio button group
            key = f"q_{q_data['id']}" 
            
            # The radio button selection
            choice = st.radio(
                label="Choose One:",
                options=q_data['choices'],
                key=key,
                index=None, # Starts with no selection
                label_visibility="collapsed"
            )
            quiz_submission[key] = choice
            
        st.write("---")
        submit_button = st.form_submit_button("Determine Archetype")
    
    # Process the form submission
    if submit_button:
        # Check if all questions were answered
        if all(choice is not None for choice in quiz_submission.values()):
            
            # 1. Calculate the raw scores
            archetype_scores = {}
            for choice in quiz_submission.values():
                archetype = CHARACTERS.get(choice)
                if archetype:
                    archetype_scores[archetype] = archetype_scores.get(archetype, 0) + 1
            
            # 2. Store the calculated scores in session state
            st.session_state.quiz_results[current_user] = archetype_scores
            st.success("Archetype profile successfully updated! Check your results above.")
            # Rerun the app to show the updated dashboard with results
            st.rerun() 
            
        else:
            st.error("Please answer all questions before submitting.")


def show_dashboard():
    """
    Display the logged-in user's dashboard, quiz, and results.
    """
    current_user = st.session_state.current_user
    st.title("🏛️ Citizen Wellness Portal™")
    st.success(f"Welcome back, **{current_user}**! Your Algorithmic Satisfaction Metrics are ready.")

    # Check if the user has completed the quiz
    user_results = st.session_state.quiz_results.get(current_user, {})
    primary_archetype, max_score = calculate_archetype(user_results)

    if max_score > 0:
        # Display Results
        st.subheader("Your Archetype Profile")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(label="Primary Archetype", value=primary_archetype)
        with col2:
            st.metric(label="Archetype Score", value=f"{max_score} / {len(ARCHETYPE_QUESTIONS)}")

        st.info(f"Based on your choices, you are most aligned with the **{primary_archetype}** archetype.")
        
        # Display detailed scores in an expander
        with st.expander("View Full Score Breakdown"):
            st.dataframe(
                data={"Archetype": list(user_results.keys()), "Score": list(user_results.values())},
                use_container_width=True
            )

    st.write("---")
    
    # Show the Quiz
    show_quiz()
    
    st.write("---")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun() 


# ─────────────────────────────────────────────────────────────────────────
# MAIN APPLICATION LOGIC
# ─────────────────────────────────────────────────────────────────────────

def main():
    """
    Main application entry point.
    """
    
    # TEMPORARY DEBUG INFO (optional)
    # with st.sidebar:
    #     st.write("🔧 Debug: Session State")
    #     st.write(dict(st.session_state))
    
    st.title("🏛️ Citizen Wellness Portal™")
    st.caption("*The Algorithm welcomes you.*")
    
    if st.session_state.get('logged_in', False):
        show_dashboard()
    else:
        # Default to the Login tab unless we just registered
        default_tab = 0 if not st.session_state.get('login_tab_selected') else 1 
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            show_login_form()
        with tab2:
            show_registration_form()
            
        # Reset the flag after showing the tabs
        if 'login_tab_selected' in st.session_state:
            del st.session_state.login_tab_selected


# ─────────────────────────────────────────────────────────────────────────
# RUN THE APP
# ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()