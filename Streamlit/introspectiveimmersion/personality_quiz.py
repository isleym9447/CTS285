# ═══════════════════════════════════════════════════════════════════════
#  pages/2_Personality_Quiz.py - MASTER TROPE QUIZ
#  Handles Trope Data, Scoring, and Quiz View
# ═══════════════════════════════════════════════════════════════════════

import streamlit as st

# ─────────────────────────────────────────────────────────────────────────
# SECURITY CHECK
# We rely on the session state initialized in the main app.py file
# ─────────────────────────────────────────────────────────────────────────
if not st.session_state.get('logged_in', False):
    st.error("Access Denied. Please use the Home page to log in.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────
# TROPE QUIZ DATA STRUCTURES
# ─────────────────────────────────────────────────────────────────────────

# Maps choices to their underlying trope
TROPE_MAPPING = {
    # Games
    "Skyrim": "Chosen One",
    "Cyberpunk 2077": "Anti-Hero",
    "Fallout 4": "Survivor",
    "Mass Effect": "Found Family",
    "Baldur's Gate 3": "Enemies to Lovers",
    "L.A. Noire": "The Whodunit",
    "Final Fantasy VII": "The Rebellion",
    "Life is Strange": "Time Travel / Multiverse",
    
    # Movies
    "Harry Potter": "Chosen One",
    "John Wick": "Anti-Hero",
    "A Quiet Place": "Survivor",
    "Star Trek": "Found Family",
    "Pride & Prejudice": "Enemies to Lovers",
    "Knives Out": "The Whodunit",
    "The Hunger Games": "The Rebellion",
    "Back to the Future": "Time Travel / Multiverse",
    
    # Books
    "Dune": "Chosen One",
    "The Witcher": "Anti-Hero",
    "The Shining": "Survivor",
    "Six of Crows": "Found Family",
    "Iron Flame": "Enemies to Lovers",
    "The Adventures of Sherlock Holmes": "The Whodunit",
    "Red Rising": "The Rebellion",
    "Dark Matter": "Time Travel / Multiverse",
    
    # TV Shows
    "Buffy the Vampire Slayer": "Chosen One",
    "Breaking Bad": "Anti-Hero",
    "Lost": "Survivor",
    "Psych": "Found Family",
    "Bridgerton": "Enemies to Lovers",
    "True Detective": "The Whodunit",
    "Andor": "The Rebellion",
    "Doctor Who": "Time Travel / Multiverse",

    # Graphic Novels
    "Invincible": "Chosen One",
    "The Punisher": "Anti-Hero",
    "Y: The Last Man": "Survivor",
    "Saga": "Found Family",
    "Lore Olympus": "Enemies to Lovers",
    "Batman: The Long Halloween": "The Whodunit",
    "V for Vendetta": "The Rebellion",
    "Paper Girls": "Time Travel / Multiverse",

    # Anime
    "Jujutsu Kaisen": "Chosen One",
    "Death Note": "Anti-Hero",
    "Attack on Titan": "Survivor",
    "One Piece": "Found Family",
    "Kaguya-sama: Love Is War": "Enemies to Lovers",
    "Monster": "The Whodunit",
    "Code Geass": "The Rebellion",
    "Steins;Gate": "Time Travel / Multiverse",
}

TROPE_QUESTIONS = [
    {
        "id": 1,
        "question": "Pick a Game world you would rather inhabit.",
        "choices": ["Skyrim", "Cyberpunk 2077", "Fallout 4", "Mass Effect", "Baldur's Gate 3", "L.A. Noire", "Final Fantasy VII", "Life is Strange"]
    },
    {
        "id": 2,
        "question": "Pick a Movie whose central conflict is most interesting to you.",
        "choices": ["Harry Potter", "John Wick", "A Quiet Place", "Star Trek", "Pride & Prejudice", "Knives Out", "The Hunger Games", "Back to the Future"]
    },
    {
        "id": 3,
        "question": "Pick a Book whose theme resonates most deeply.",
        "choices": ["Dune", "The Witcher", "The Shining", "Six of Crows", "Iron Flame", "The Adventures of Sherlock Holmes", "Red Rising", "Dark Matter"]
    },
    {
        "id": 4,
        "question": "Pick a TV Show that best reflects your preferred drama.",
        "choices": ["Buffy the Vampire Slayer", "Breaking Bad", "Lost", "Psych", "Bridgerton", "True Detective", "Andor", "Doctor Who"]
    },
    {
        "id": 5,
        "question": "Pick a Graphic Novel that represents your favorite genre.",
        "choices": ["Invincible", "The Punisher", "Y: The Last Man", "Survivor", "Saga", "Lore Olympus", "Batman: The Long Halloween", "V for Vendetta", "Paper Girls"]
    },
    {
        "id": 6,
        "question": "Pick an Anime with a plot that captivates you.",
        "choices": ["Jujutsu Kaisen", "Death Note", "Attack on Titan", "Survivor", "One Piece", "Kaguya-sama: Love Is War", "Monster", "Code Geass", "Steins;Gate"]
    },
]

# ─────────────────────────────────────────────────────────────────────────
# TROPE RESULT BLURBS
# ─────────────────────────────────────────────────────────────────────────

TROPE_BLURBS = {
    "Found Family": "You like works of fiction with Found Family because you find comfort and strength in the belief that belonging is earned, not just given. Your life philosophy centers on the loyalty and unconditional support of the bonds you choose—a guiding path you forge with others who genuinely see and accept you.",
    "Enemies to Lovers": "You are drawn to Enemies to Lovers because you understand that the strongest, most passionate connections often emerge from genuine friction and the dismantling of deeply held misconceptions. You appreciate the catharsis of two people being forced to acknowledge and embrace the complexity beneath the surface, proving that the line between hate and obsession is thrillingly thin.",
    "Anti-Hero": "You connect with The Anti-Hero because you reject the rigid simplicity of black-and-white morality and find truth in the struggle of the morally grey. Your heart is drawn to stories where necessity and human weakness drive choices, reminding you that sometimes, the most effective path to an honorable goal is through an inherently complicated soul.",
    "Survivor": "You are fascinated by The Survivor because you find profound validation in the resilience of the human spirit when all external comforts are stripped away. These stories speak to your inner certainty that you possess the enduring strength to rebuild, to adapt, and to find meaning even in the absolute void of isolation or a broken world.",
    "Chosen One": "You are drawn to The Chosen One because you find both awe and validation in the idea that one person's life can hold immense, world-altering significance. These stories speak to your desire to believe in a higher purpose and acknowledge the unique, often burdensome, potential you carry—reminding you that your personal journey is intrinsically linked to a destiny larger than yourself.",
    "The Whodunit": "You love The Whodunit because you crave the satisfaction of imposing order on chaos and proving that intellect is the ultimate tool for navigating the world. Your internal comfort comes from the realization that every difficult situation has a logical solution, and all you need is enough patience and sharp observation to piece together the truth.",
    "The Rebellion": "You resonate with The Rebellion because you fundamentally believe in the moral imperative to challenge systems of injustice and stand up for the inherent dignity of all people. These stories reflect your unshakeable optimism that collective action, courage, and a shared vision of freedom can—and must—defeat overwhelming tyranny.",
    "Time Travel / Multiverse": "You are captivated by Time Travel or the Multiverse because you constantly wrestle with the weight of consequence, finding comfort in exploring the what-ifs and the infinite potential of alternate choices. These concepts satisfy your introspective need to understand how small decisions ripple through reality, prompting you to live more intentionally in the single timeline you inhabit.",
}


# ─────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────

def calculate_trope(results: dict[str, int]) -> tuple[str, int]:
    """Calculates the user's primary trope from the quiz results."""
    if not results or all(v == 0 for v in results.values()):
        return ("Undetermined", 0)
    
    primary_trope = max(results, key=results.get)
    max_score = results[primary_trope]
    
    tied_tropes = [k for k, v in results.items() if v == max_score]
    if len(tied_tropes) > 1:
        return (f"Tied ({' & '.join(tied_tropes)})", max_score)
        
    return (primary_trope, max_score)


# ─────────────────────────────────────────────────────────────────────────
# VIEW FUNCTION (The Page Content)
# ─────────────────────────────────────────────────────────────────────────

def show_personality_page():
    """Page view for the Master Trope Personality Quiz."""
    current_user = st.session_state.current_user
    st.title("Master Trope Personality Quiz")
    st.caption("Based on your fictional preferences, we determine your preferred narrative role.")

    # --- Display Results ---
    user_results = st.session_state.get('trope_results', {}).get(current_user, {})
    # This requires the calculate_trope helper function to be defined elsewhere in the file.
    primary_trope, max_score = calculate_trope(user_results) 

    if max_score > 0:
        st.subheader("Your Trope Profile")
        
        # Fancy display for the result
        st.markdown(f"""
        ## Your defining narrative is the **{primary_trope}** Trope!
        """)
        
        # Display the blurb associated with the primary trope
        blurb = TROPE_BLURBS.get(primary_trope, "Analysis pending. This trope has an unknown resonance.")
        st.success(f"**Your Narrative Resonance:** {blurb}")

        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(label="Primary Trope Score", value=f"{max_score} / {len(TROPE_QUESTIONS)}")
        with col2:
            st.metric(label="Total Questions Answered", value=len(TROPE_QUESTIONS))

        st.caption("Review your score breakdown below.")
        
        with st.expander("View Full Score Breakdown"):
            st.dataframe(
                data={"Trope": list(user_results.keys()), "Score": list(user_results.values())},
                use_container_width=True
            )
    
    st.write("---")
    
    # --- Display Quiz Form ---
    st.header("Trope Profiling Quiz")
    st.markdown("### Choose the fictional world that appeals most to you.")
    
    with st.form("trope_quiz_form"):
        quiz_submission = {}
        
        for q_data in TROPE_QUESTIONS:
            st.markdown(f"**Q{q_data['id']}.** *{q_data['question']}*")
            key = f"tq_{q_data['id']}" 
            
            choice = st.radio(
                label="Choose One:",
                options=q_data['choices'],
                key=key,
                index=None,
                label_visibility="collapsed"
            )
            quiz_submission[key] = choice
            
        st.write("---")
        submit_button = st.form_submit_button("Determine Trope")
    
    if submit_button:
        if all(choice is not None for choice in quiz_submission.values()):
            trope_scores = {}
            for choice in quiz_submission.values():
                trope = TROPE_MAPPING.get(choice)
                if trope:
                    trope_scores[trope] = trope_scores.get(trope, 0) + 1
            
            # Store the trope results in the global session state
            if 'trope_results' not in st.session_state:
                 st.session_state.trope_results = {}
            st.session_state.trope_results[current_user] = trope_scores
            
            st.success("Trope profile successfully updated! Check your results above.")
            st.rerun() 
            
        else:
            st.error("Please answer all questions before submitting.")

# ─────────────────────────────────────────────────────────────────────────
# PAGE EXECUTION
# ─────────────────────────────────────────────────────────────────────────

show_personality_page()