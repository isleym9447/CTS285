# ═══════════════════════════════════════════════════════════════════════
# pages/1_Archetype_Quiz.py
# ═══════════════════════════════════════════════════════════════════════

import streamlit as st

# ─────────────────────────────────────────────────────────────────────────
# SECURITY CHECK & INITIAL SETUP
# ─────────────────────────────────────────────────────────────────────────

# This check prevents direct access if the user hasn't logged in via app.py
if not st.session_state.get('logged_in', False):
    st.error("Please log in via the main page to access the quizzes.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────
# QUIZ DATA STRUCTURES (Copied from original app.py)
# ─────────────────────────────────────────────────────────────────────────

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
        "question": "If you were a Ninja, who would be your ideal sensei from Naruto?",
        "choices": ["Naruto Uzumaki", "Sasuke Uchiha", "Sakura Haruno", "Kakashi Hatake", "Itachi Uchiha"]
    },
    {
        "id": 7,
        "question": "In the world of JJK, which character would you most likely follow into a fight?",
        "choices": ["Yuji Itadori", "Megumi Fushiguro", "Nobara Kugisaki", "Satoru Gojo", "Suguru Geto"]
    },
]

# ─────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS (Copied from original app.py)
# ─────────────────────────────────────────────────────────────────────────

def calculate_archetype(results: dict[str, int]) -> tuple[str, int]:
    """
    Calculates the user's primary archetype from the quiz results.
    """
    if not results or all(v == 0 for v in results.values()):
        return ("Undetermined", 0)
    
    primary_archetype = max(results, key=results.get)
    max_score = results[primary_archetype]
    
    tied_archetypes = [k for k, v in results.items() if v == max_score]
    if len(tied_archetypes) > 1:
        return (f"Tied ({' & '.join(tied_archetypes)})", max_score)
        
    return (primary_archetype, max_score)


# ─────────────────────────────────────────────────────────────────────────
# VIEW FUNCTIONS (Dashboard and Quiz)
# ─────────────────────────────────────────────────────────────────────────

def show_quiz():
    """
    Display the character preference quiz and process submissions.
    """
    st.header("Archetype Profiling")
    st.markdown("### Select your favorite character from each set.")
    
    current_user = st.session_state.current_user
    
    with st.form("archetype_quiz_form"):
        quiz_submission = {}
        
        for q_data in ARCHETYPE_QUESTIONS:
            st.markdown(f"**Q{q_data['id']}.** *{q_data['question']}*")
            key = f"q_{q_data['id']}" 
            
            choice = st.radio(
                label="Choose One:",
                options=q_data['choices'],
                key=key,
                index=None,
                label_visibility="collapsed"
            )
            quiz_submission[key] = choice
            
        st.write("---")
        submit_button = st.form_submit_button("Determine Archetype")
    
    if submit_button:
        if all(choice is not None for choice in quiz_submission.values()):
            
            archetype_scores = {}
            for choice in quiz_submission.values():
                archetype = CHARACTERS.get(choice)
                if archetype:
                    archetype_scores[archetype] = archetype_scores.get(archetype, 0) + 1
            
            st.session_state.quiz_results[current_user] = archetype_scores
            st.success("Archetype profile successfully updated! Check your results above.")
            st.rerun() 
            
        else:
            st.error("Please answer all questions before submitting.")


def show_dashboard():
    """
    Display the logged-in user's dashboard, quiz, and results.
    This version is slightly modified for the multi-page context.
    """
    current_user = st.session_state.current_user
    st.title("Archetype Quiz Dashboard")
    st.caption(f"Welcome, **{current_user}**! Test your preferences below.")

    user_results = st.session_state.quiz_results.get(current_user, {})
    primary_archetype, max_score = calculate_archetype(user_results)

    if max_score > 0:
        st.subheader("Your Archetype Profile")
        
        # -----------------------------------------------------------------
        # MODIFIED: Use markdown for bigger, bolder display of the result
        # -----------------------------------------------------------------
        st.markdown(f"""
        ## You most align with the **{primary_archetype}** Archetype!
        """)
        # -----------------------------------------------------------------
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(label="Primary Archetype Score", value=f"{max_score} / {len(ARCHETYPE_QUESTIONS)}")
        with col2:
            st.metric(label="Total Questions Answered", value=len(ARCHETYPE_QUESTIONS))

        st.caption("Review your score breakdown below.")
        
        with st.expander("View Full Score Breakdown"):
            st.dataframe(
                data={"Archetype": list(user_results.keys()), "Score": list(user_results.values())},
                use_container_width=True
            )

    st.write("---")
    
    show_quiz()
    
    st.write("---")
    
    # Logout button (kept here for convenience, though main app handles navigation)
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun() 


# ─────────────────────────────────────────────────────────────────────────
# PAGE EXECUTION
# ─────────────────────────────────────────────────────────────────────────

show_dashboard()