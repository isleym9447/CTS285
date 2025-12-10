# Introspective Immersion #
## A Streamlit Application for Archetype & Personality Exploration ##

Introspective Immersion is an interactive Streamlit web application designed to help users explore their personal archetypes, discover personality insights, and receive tailored media recommendations based on their results. The experience blends introspection, storytelling, and design into a smooth, gamified user experience.

# Features #
## User Login System ##

Simple username‐based login

Personalized session state tracking

Unique results per user

## Archetype Quiz ##

Users answer a set of questions

Scores map to one of the main archetypes:

Hero

Innocent

Anti-Hero

Mentor

Villain

Results unlock the corresponding profile image

Stored in session_state per user

## Personality Quiz ##

Additional personality-driven choices

Used to generate deeper recommendation logic

Results stored individually per user

## Profile Page ##
  
Displays username

Shows archetype image once unlocked

Shows quiz completion status

Placeholder image if quizzes are not yet taken

## Recommendations ##

Generates personalized game, movie, show, anime, and book recommendations

Pulled from logic in reccomendation.py

Tied to archetype + personality results

## Project Structure ##
.
├── app.py                 # Main login/home page
├── profile.py (or /pages/4_Profile.py)
├── archetype_quiz.py
├── personality_quiz.py
├── reccomendation.py
├── hero.png
├── innocent.png
├── antihero.png
├── mentor.png
├── villian.png
└── README.md


If using Streamlit’s multipage mode, place all pages inside a folder named:

pages/


Example:

pages/
    1_Archetype_Quiz.py
    2_Personality_Quiz.py
    3_Recommendation.py
    4_Profile.py

# Installation & Setup #
## 1️⃣ Clone the repository ##
git clone https://github.com/your-username/introspective-immersion.git
cd introspective-immersion

## 2️⃣ Create a virtual environment (optional but recommended) ##
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

## 3️⃣ Install dependencies ##
pip install -r requirements.txt


Or if you don’t have a requirements file yet:

pip install streamlit

## 4️⃣ Run the app ##
streamlit run app.py


If using multipage mode, Streamlit will automatically load everything inside the pages/ directory.

## Archetype Images ##

The app looks for the following image files:

hero.png
innocent.png
antihero.png
mentor.png
villian.png


These must be in the same directory as profile.py or referenced with correct paths.

## Data & Session State ##

This app stores all quiz progress in st.session_state, including:

current_user

quiz_results for each user

personality_results

archetype outcomes

login status

No external database is required.

## Future Features (Optional Ideas) ##

Save user profiles to a real database (Firebase, Supabase, SQLite)

Add personality type icons

Add animated transitions between quiz questions

Dark mode / theme customization

Dashboard analytics for traits & archetypes

Journal or diary module
