# AlgoCratic Futures - Citizen Wellness Portal™ Development Process

## Project Goal
To build a secure login/registration system and a personality profiling quiz (Archetype Profiler) using Streamlit and Python.

## Streamlit Learning Notes

| Concept | Description/Function | Application in this Project |
| :--- | :--- | :--- |
| `st.session_state` | A dictionary-like object used to preserve state between script reruns. Essential for tracking user login status and storing quiz results. | Used for `logged_in`, `current_user`, `users` (registration data), and `quiz_results`. |
| `st.form()` | Creates a block that prevents the app from rerunning on every widget interaction inside it (e.g., every keystroke). The app only reruns when the form's `st.form_submit_button` is pressed. | Used for `login_form`, `registration_form`, and the `archetype_quiz_form` to manage user input efficiently. |
| `st.rerun()` | Forces the entire Streamlit script to re-execute from the top immediately. | Used after successful login/logout and after quiz submission to refresh the UI and show the dashboard/results. |
| `st.tabs()` | Used to create distinct, switchable sections of the app within the main page. | Used to separate the Login and Registration forms when the user is not logged in. |

## Things That Surprised/Confused Me

1.  **Stateless Nature:** Streamlit's fundamental behavior is to re-run the script from top to bottom on *every* user interaction (button click, text input change). This required immediate adoption of `st.session_state` to prevent losing login and registration data.
2.  **Form Scope:** Initially, I tried to implement the login without `st.form()`, which caused the entire app to re-run on every character typed into the password field. Using `st.form()` was crucial to prevent this behavior and ensure a smooth login experience.

## Implementation Details

1.  **User Data:** A simple dictionary (`st.session_state.users`) combined with basic SHA-256 hashing (`hashlib`) was used for credential storage and validation.
2.  **Quiz Logic:** The quiz uses a data-driven approach (`CHARACTERS` and `ARCHETYPE_QUESTIONS` dictionaries). The `show_quiz()` function iterates through `ARCHETYPE_QUESTIONS`, collecting responses using `st.radio` within a single `st.form()` submission.
3.  **Scoring:** The `calculate_archetype()` function counts character selections by mapping the chosen character back to its underlying archetype via the `CHARACTERS` dictionary, ensuring accurate scoring and handling potential ties.