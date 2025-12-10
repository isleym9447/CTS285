# ═══════════════════════════════════════════════════════════════════════
#  profile.py - USER PROFILE PAGE
# ═══════════════════════════════════════════════════════════════════════

import streamlit as st
import base64
# NOTE: Ensure you include the definition of calculate_archetype 
# or import it from a shared utility file if you move it out of app.py.
# For simplicity, we define a basic version here:

def calculate_archetype_name(results: dict[str, int]) -> str:
    """Calculates and returns ONLY the primary archetype name (or Undetermined)."""
    if not results or all(v == 0 for v in results.values()):
        return "Undetermined"
    
    primary_archetype = max(results, key=results.get)
    return primary_archetype

def get_base64_of_bin_file(bin_file):
    """Reads a local file and encodes it to a base64 string."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# ─────────────────────────────────────────────────────────────────────────
# SECURITY CHECK
# ─────────────────────────────────────────────────────────────────────────
if not st.session_state.get('logged_in', False):
    st.error("Access Denied. Please use the Home page to log in.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────
# PROFILE VIEW
# ─────────────────────────────────────────────────────────────────────────

def show_profile_page():
    current_user = st.session_state.current_user
    st.title("Profile")
    st.subheader(f"Name: {current_user}")
    st.write("---")

    # 1. Check Archetype Result
    user_quiz_results = st.session_state.get('quiz_results', {}).get(current_user, {})
    primary_archetype = calculate_archetype_name(user_quiz_results)
    
    # 2. Determine Image Path
    IMAGE_SIZE_STYLE = "max-width: 250px; height: auto; border-radius: 10px;"
    
    if primary_archetype == "Undetermined":
        display_text = "Take Archetype Quiz to unlock!"
        image_path = None # No specific image
    elif primary_archetype.startswith("Tied"):
        # If tied, pick the first one for the photo display
        trope_name = primary_archetype.split('(')[1].split(' & ')[0].strip()
        display_text = f"Primary Archetype: {primary_archetype}"
        image_path = f"{trope_name.lower()}.png" # e.g., hero.png
    else:
        trope_name = primary_archetype
        display_text = f"Primary Archetype: {primary_archetype}"
        image_path = f"{trope_name.lower()}.png" # e.g., hero.png


    # --- PROFILE PHOTO DISPLAY ---
    
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        if image_path:
            base64_image = get_base64_of_bin_file(image_path)
            
            if base64_image:
                st.markdown(f"""
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="data:image/png;base64,{base64_image}" 
                             alt="{trope_name} Profile Photo" 
                             style="{IMAGE_SIZE_STYLE}">
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"Image not found at expected path: {image_path}")
        else:
            # Placeholder for 'Undetermined'
            st.markdown(f"""
                <div style="
                    text-align: center; 
                    margin: 50px 0; 
                    padding: 20px; 
                    border: 2px dashed #808080; 
                    border-radius: 10px;">
                    <p style='font-size: 1.2em; font-weight: bold;'>{display_text}</p>
                </div>
            """, unsafe_allow_html=True)

    st.write("---")
    st.info(display_text)
    
    # You might want to add more profile details here
    st.markdown("### Profile Metrics")
    st.metric("Registration Status", "Active")
    st.metric("Archetype Quiz Status", "Completed" if primary_archetype != "Undetermined" else "Pending")
    


# ─────────────────────────────────────────────────────────────────────────
# PAGE EXECUTION
# ─────────────────────────────────────────────────────────────────────────

show_profile_page()