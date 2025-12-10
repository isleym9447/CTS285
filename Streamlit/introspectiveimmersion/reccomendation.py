# ═══════════════════════════════════════════════════════════════════════
#  pages/3_Recommendation.py - RECOMMENDATION ENGINE
#  Pulls trope results and suggests media based on the user's preference.
# ═══════════════════════════════════════════════════════════════════════

import streamlit as st
import random # Needed to pick random items

# ─────────────────────────────────────────────────────────────────────────
# SECURITY CHECK
# ─────────────────────────────────────────────────────────────────────────
if not st.session_state.get('logged_in', False):
    st.error("🔒 Access Denied. Please use the Home page to log in.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────
# HELPER FUNCTION (To calculate primary trope from existing results)
# NOTE: This function is duplicated here to ensure the page can calculate
# the current result without importing the massive code from the quiz file.
# ─────────────────────────────────────────────────────────────────────────

def calculate_trope(results: dict[str, int]) -> str:
    """Calculates and returns ONLY the user's primary trope name."""
    if not results or all(v == 0 for v in results.values()):
        return "Undetermined"
    
    primary_trope = max(results, key=results.get)
    max_score = results[primary_trope]
    
    # Handle ties by prioritizing the first one alphabetically for simplicity
    tied_tropes = [k for k, v in results.items() if v == max_score]
    if len(tied_tropes) > 1:
        return f"Tied ({' & '.join(tied_tropes)})"
        
    return primary_trope


# ─────────────────────────────────────────────────────────────────────────
# MASTER TROPE RECOMMENDATION DATA
# ─────────────────────────────────────────────────────────────────────────

# Structure: {Trope: {Category: [Item1, Item2, ...], ...}, ...}
TROPE_RECOMMENDATIONS = {
    "Found Family": {
        "Games": ["Mass Effect Trilogy", "Dragon Age: Inquisition", "Final Fantasy XV", "Baldur’s Gate 3", "Fire Emblem: Three Houses", "Destiny 2", "The Last of Us (Joel/Ellie counts as family)", "Tales of Vesperia", "Overwatch", "Persona 5"],
        "Movies": ["Guardians of the Galaxy", "The Avengers", "The Fast and the Furious", "Star Wars: A New Hope", "Atlantis: The Lost Empire", "The Goonies", "Big Hero 6", "Ocean’s Eleven", "X-Men (2000)", "The Lord of the Rings Trilogy"],
        "TV Shows": ["Firefly", "Star Trek: Discovery", "Stranger Things", "The Mandalorian", "Avatar: The Last Airbender", "Buffy the Vampire Slayer", "The Umbrella Academy", "Leverage", "Critical Role (Campaign 2)", "Teen Titans"],
        "Books": ["The Raven Cycle — Maggie Stiefvater", "Six of Crows — Leigh Bardugo", "Percy Jackson — Rick Riordan", "The Hobbit — J.R.R. Tolkien", "The Expanse — James S.A. Corey", "Red Rising — Pierce Brown", "The Lunar Chronicles — Marissa Meyer", "Mistborn — Brandon Sanderson", "The Golden Compass — Philip Pullman", "It — Stephen King"],
        "Graphic Novels": ["Saga", "The Umbrella Academy", "Runaways", "Paper Girls", "Young Avengers", "Gotham Academy", "Lumberjanes", "Teen Titans", "Invincible", "Rat Queens"],
        "Anime": ["Fullmetal Alchemist: Brotherhood", "One Piece", "Haikyuu!!", "My Hero Academia", "Jujutsu Kaisen", "Naruto", "Demon Slayer", "Cowboy Bebop", "Fairy Tail", "Attack on Titan"],
    },
    "Enemies to Lovers": {
        "Games": ["Dragon Age 2 (Fenris/Hawke dynamic)", "Final Fantasy VIII", "Fire Emblem: Awakening", "Baldur’s Gate 3 (Lae’zel route)", "Mass Effect (Jack/Shepard hostile start)", "The Witcher 3 (Yen & Geralt’s chaotic energy)", "Dragon Age: Inquisition (Cassandra initial hostility)", "Hades (Zagreus & Megaera)", "FFVII Remake (Cloud & Tifa/Reno moments)", "Persona 4 Arena (Yu vs Adachi rivalry)"],
        "Movies": ["Pride and Prejudice", "Mr. & Mrs. Smith", "10 Things I Hate About You", "The Proposal", "Star Wars (Kylo Ren & Rey)", "The Mummy (Evy & Rick banter)", "Howl’s Moving Castle", "Cruel Intentions", "Warm Bodies", "Romancing the Stone"],
        "TV Shows": ["Bridgerton (S1, S2)", "The Vampire Diaries", "Killing Eve", "Avatar: The Last Airbender (Zuko & Katara fandom staple)", "Lucifer", "Outlander", "The Expanse (Naomi & Amos tension)", "Once Upon a Time", "Shadow and Bone", "The 100"],
        "Books": ["Red White & Royal Blue", "Serpent & Dove", "The Cruel Prince", "These Violent Delights", "From Blood and Ash", "Shatter Me", "The Hating Game", "The Folk of the Air (Jude/Cardan)", "The Wrath & The Dawn", "Twilight (technically)"],
        "Graphic Novels": ["Monstress", "Lore Olympus", "Saga", "Heartstopper (light enemies start)", "Persephone (Rachel Smythe’s other work)", "Poison Ivy & Harley Quinn (slow antagonistic start)", "X-Men: Emma Frost/Scott Summers arc", "Rat Queens (romantic tension arcs)", "Wicked + Divine", "Blackbird"],
        "Anime": ["Inuyasha", "Kaguya-sama: Love is War", "Yona of the Dawn", "Noragami", "Fate/Stay Night", "Darling in the Franxx", "K Project", "Bleach (Rukia/Ichigo rivalry start)", "Sword Art Online (Asuna hostile early)", "Attack on Titan (Hange/Levi tension)"],
    },
    "Anti-Hero": {
        "Games": ["Cyberpunk 2077", "The Witcher 3", "Dishonored", "Red Dead Redemption 2", "GTA V", "Assassin’s Creed (Ezio, Altair)", "Dragon Age: Origins", "Mass Effect Renegade path", "Kingdom Come: Deliverance", "Vampyr"],
        "Movies": ["Deadpool", "Joker", "V for Vendetta", "John Wick", "Venom", "Logan", "Fight Club", "The Dark Knight", "Mad Max: Fury Road", "Léon: The Professional"],
        "TV Shows": ["Breaking Bad", "The Boys", "Peaky Blinders", "Daredevil", "Jessica Jones", "Hannibal", "Sons of Anarchy", "The Punisher", "True Detective", "Vikings"],
        "Books": ["The First Law Trilogy — Joe Abercrombie", "The Witcher books", "The Girl with the Dragon Tattoo", "American Psycho", "Red Rising (Darrow early arc)", "The Road", "Interview with the Vampire", "Gone Girl", "The Black Company", "Mistborn (Kelsier)"],
        "Graphic Novels": ["Watchmen", "V for Vendetta", "Sin City", "The Punisher", "Constantine: Hellblazer", "Moon Knight", "Spawn", "The Crow", "Deadpool", "Sandman (morally grey gods everywhere)"],
        "Anime": ["Tokyo Ghoul", "Psycho-Pass", "Death Note", "Jujutsu Kaisen (Geto, Sukuna, Megumi arcs)", "Attack on Titan", "Black Lagoon", "Vinland Saga", "Parasyte", "Code Geass", "Dororo"],
    },
    "Survivor": {
        "Games": ["The Last of Us", "Resident Evil 2", "Metro Exodus", "Fallout: New Vegas", "Subnautica", "The Forest", "Outlast", "Dead Space", "SOMA", "Days Gone"],
        "Movies": ["28 Days Later", "The Revenant", "Cast Away", "The Road", "The Martian", "A Quiet Place", "I Am Legend", "Train to Busan", "Gravity", "Bird Box"],
        "TV Shows": ["The Walking Dead", "The Last of Us (HBO)", "Lost", "The Rain", "Station Eleven", "Snowpiercer", "The 100", "Black Summer", "Z Nation", "See"],
        "Books": ["The Road — Cormac McCarthy", "The Stand — Stephen King", "The Girl With All the Gifts", "Station Eleven", "Lord of the Flies", "Life of Pi", "The Hunger Games", "The Passage", "The Knife of Never Letting Go", "Metro 2033"],
        "Graphic Novels": ["The Walking Dead", "Y: The Last Man", "Sweet Tooth", "Wytches", "Low", "The Massive", "DMZ", "Monstress", "Oblivion Song", "Gideon Falls"],
        "Anime": ["Attack on Titan", "The Promised Neverland", "High-Rise Invasion", "7 Seeds", "Tokyo Magnitude 8.0", "Parasyte", "Deadman Wonderland", "Coppelion", "Ajin", "Psycho-Pass"],
    },
    "Chosen One": {
        "Games": ["The Legend of Zelda: Ocarina of Time (Link as the Hero of Time)", "Final Fantasy VII (Cloud’s destiny and Jenova ties)", "Dragon Age: Inquisition (The Inquisitor)", "Horizon Zero Dawn (Aloy as the key to Zero Dawn)", "Kingdom Hearts (Sora as Keyblade wielder)", "Mass Effect (Shepard chosen by the Protheans)", "God of War (2018) (Atreus/Loki prophecy)", "The Witcher 3 (Ciri as the Child of Destiny)", "Skyrim (The Dragonborn)", "Fable III (Child of the Hero of Albion)"],
        "Movies": ["Harry Potter Series", "Star Wars: The Force Awakens (Rey)", "The Matrix Trilogy (Neo, “The One”)", "Dune (2021) (Paul Atreides, Lisan al-Gaib)", "The Lord of the Rings (Frodo as Ring-Bearer)", "Kung Fu Panda (Po as the Dragon Warrior)", "Moana (Chosen by the ocean)", "The Dark Tower", "The Chronicles of Narnia: The Lion, the Witch and the Wardrobe (Pevensies as prophesied monarchs)", "Percy Jackson: Sea of Monsters (Percy as a child of prophecy)"],
        "TV Shows": ["Buffy the Vampire Slayer (The Slayer)", "Avatar: The Last Airbender (Aang)", "Supernatural (Sam Winchester demon-blood prophecy)", "Stranger Things (El as the weapon against the Upside Down)", "The Witcher (Ciri, in show form too)", "The Magicians (Quentin Coldwater)", "Shadow and Bone (Alina Starkov, Sun Summoner)", "The Wheel of Time (Rand al’Thor, Dragon Reborn)", "Merlin (Arthur’s prophesied future)", "His Dark Materials (Lyra Silvertongue)"],
        "Books": ["Harry Potter — J.K. Rowling", "Percy Jackson & The Olympians — Rick Riordan", "The Wheel of Time — Robert Jordan", "Mistborn — Brandon Sanderson (Vin’s prophesied role)", "The Hunger Games — Suzanne Collins (Katniss as the Mockingjay)", "The Name of the Wind — Patrick Rothfuss", "Eragon — Christopher Paolini", "Sabriel — Garth Nix", "Red Queen — Victoria Aveyard", "The Mortal Instruments — Cassandra Clare"],
        "Graphic Novels": ["Hellboy (Anung Un Rama destiny)", "Saga (Hazel as a child of forbidden prophecy)", "Monstress (Maika Halfwolf destiny-bound)", "Sandman (Dream’s chosen mortals & cosmic fate arcs)", "X-Men: Dark Phoenix Saga (Jean Grey chosen by the Phoenix Force)", "Fables (Bigby & Snow’s prophecy children)", "Invincible (Mark Grayson as the chosen Viltrumite hybrid)", "Young Avengers: Wiccan", "Shazam! (Chosen by the Wizard)", "Sweet Tooth (Gus as a foretold hybrid)"],
        "Anime": ["Naruto (Child of Prophecy)", "Attack on Titan (Eren’s Founding Titan path)", "My Hero Academia (Deku and One For All)", "Demon Slayer (Tanjiro’s Sun Breathing legacy)", "Fullmetal Alchemist: Brotherhood (Edward as the pivotal catalyst)", "Fate/Stay Night (Chosen Masters/Servants dynamic)", "Jujutsu Kaisen (Yuji as Sukuna’s vessel)", "Blue Exorcist (Rin Okumura, son of Satan)", "Puella Magi Madoka Magica (Madoka’s magical fate)", "Sword Art Online (Kirito as the system-altered outlier)"],
    },
    "The Whodunit": {
        "Games": ["LA Noire", "Ace Attorney", "Return of the Obra Dinn", "Disco Elysium", "Sherlock Holmes: Crimes & Punishments", "The Vanishing of Ethan Carter", "Her Story", "Heavy Rain", "Alan Wake", "Murdered: Soul Suspect"],
        "Movies": ["Knives Out", "Clue", "Murder on the Orient Express", "Se7en", "Gone Girl", "Shutter Island", "The Girl with the Dragon Tattoo", "Zodiac", "The Nice Guys", "Prisoners"],
        "TV Shows": ["Sherlock", "True Detective", "Broadchurch", "Criminal Minds", "The Mentalist", "Elementary", "Hannibal", "Mare of Easttown", "Luther", "Monk"],
        "Books": ["Sherlock Holmes — Arthur Conan Doyle", "And Then There Were None — Agatha Christie", "The Girl with the Dragon Tattoo", "The Da Vinci Code", "Gone Girl", "The Name of the Rose", "Sharp Objects", "The Maltese Falcon", "Annihilation", "The Silent Patient"],
        "Graphic Novels": ["Blacksad", "Watchmen (mystery core)", "Detective Comics (Batman)", "Sin City", "From Hell", "Mind MGMT", "The Question", "Gideon Falls", "TinTin", "The Department of Truth"],
        "Anime": ["Death Note", "Monster", "Erased", "Hyouka", "Psycho-Pass", "The Millionaire Detective", "Gosick", "ID: Invaded", "Case Closed (Detective Conan)", "Paranoia Agent"],
    },
    "The Rebellion": {
        "Games": ["BioShock Infinite", "Final Fantasy VII", "Star Wars: The Old Republic", "Horizon Zero Dawn", "Dishonored", "Deus Ex: Human Revolution", "Skyrim (Stormcloak or Empire faction)", "Half-Life 2", "Red Faction: Guerrilla", "Mirror’s Edge"],
        "Movies": ["The Hunger Games", "Star Wars: Rogue One", "V for Vendetta", "The Matrix", "Snowpiercer", "Mad Max: Fury Road", "Divergent", "Equilibrium", "Les Misérables", "The Dark Knight Rises"],
        "TV Shows": ["The Handmaid’s Tale", "The 100", "Star Wars: Rebels", "The Expanse", "Andor", "Firefly", "Altered Carbon", "Snowpiercer", "Westworld", "The Man in the High Castle"],
        "Books": ["The Hunger Games", "1984", "Brave New World", "Red Rising", "Fahrenheit 451", "Legend — Marie Lu", "Divergent", "The Handmaid’s Tale", "Ready Player One", "Mistborn (skaa rebellion)"],
        "Graphic Novels": ["V for Vendetta", "Watchmen", "DMZ", "Transmetropolitan", "Y: The Last Man", "Maus", "Saga", "East of West", "Lazarus", "Monstress"],
        "Anime": ["Code Geass", "Attack on Titan", "Akame ga Kill", "Kill la Kill", "Gurren Lagann", "Guilty Crown", "Psycho-Pass", "Aldnoah.Zero", "1984 (anime film adaptation)", "Fullmetal Alchemist: Brotherhood"],
    },
    "Time Travel / Multiverse": {
        "Games": ["Life is Strange", "Dishonored 2 (time-travel mission)", "Chrono Trigger", "The Legend of Zelda: Ocarina of Time", "Kingdom Hearts", "Bioshock Infinite", "Outer Wilds", "Cyberpunk 2077: Phantom Liberty (branching split timelines)", "Fire Emblem: Awakening", "Zero Escape Trilogy"],
        "Movies": ["Interstellar", "Everything Everywhere All At Once", "Doctor Strange", "Spider-Verse", "Tenet", "Edge of Tomorrow", "Back to the Future", "Looper", "The Butterfly Effect", "Predestination"],
        "TV Shows": ["Loki", "Dark", "The OA", "Arcane (multiverse comics tie-in and time-layered lore)", "Doctor Who", "The Umbrella Academy", "Fringe", "Travelers", "12 Monkeys", "Russian Doll"],
        "Books": ["The Time Traveler’s Wife", "11/22/63 — Stephen King", "Slaughterhouse-Five", "The First Fifteen Lives of Harry August", "Recursion — Blake Crouch", "The Midnight Library", "Kindred — Octavia Butler", "Dark Matter — Blake Crouch", "Outlander", "A Wrinkle in Time"],
        "Graphic Novels": ["Watchmen", "Flashpoint", "Spider-Verse", "Paper Girls", "Saga (dimension folds)", "Umbrella Academy", "X-Men: Days of Future Past", "Chrononauts", "East of West", "Black Science"],
        "Anime": ["Steins;Gate", "Re:Zero", "Erased", "The Girl Who Leapt Through Time", "Tokyo Revengers", "Violet Evergarden Gaiden (time-frame spanning)", "Summertime Render", "Puella Magi Madoka Magica", "Your Name", "Link Click"],
    },
}

# ─────────────────────────────────────────────────────────────────────────
# PAGE EXECUTION
# ─────────────────────────────────────────────────────────────────────────

def show_recommendation_page():
    """Display recommendations based on the user's primary trope."""
    current_user = st.session_state.current_user
    st.title("🎯 Recommendation Engine")
    st.subheader(f"Recommendations for {current_user}")
    st.write("---")

    # 1. Fetch user's trope results
    user_trope_results = st.session_state.get('trope_results', {}).get(current_user, {})
    
    # 2. Calculate the primary trope
    primary_trope = calculate_trope(user_trope_results)

    if primary_trope == "Undetermined":
        st.warning("Please complete the **Personality Quiz** first to receive recommendations!")
        return
        
    if primary_trope.startswith("Tied"):
        st.info(f"Your primary interest is split: {primary_trope}. Recommendations below are based on one of your top tropes.")
        # For tied results, grab the first trope in the tie for recommendation purposes
        primary_trope = primary_trope.split('(')[1].split(' & ')[0]


    st.markdown(f"## Based on your **{primary_trope}** Trope Resonance...")
    st.write(f"You crave narratives centered around the theme of **{primary_trope}**. Here are **three randomized suggestions for every media type** to feed your passion:")

    st.write("---")
    
    # 3. Pull recommendations for the primary trope
    recommendations = TROPE_RECOMMENDATIONS.get(primary_trope)
    
    if recommendations:
        
        # Define the desired order of categories
        ordered_categories = ["Games", "Movies", "TV Shows", "Books", "Graphic Novels", "Anime"]
        
        for category in ordered_categories:
            if category in recommendations:
                item_list = recommendations[category]
                
                # Ensure we don't try to pick more items than exist (should always be 10)
                num_to_pick = min(3, len(item_list))
                
                # Pick 3 unique random items from the list
                random_items = random.sample(item_list, num_to_pick)
                
                st.markdown(f"### {category} Recommendations")
                
                # Use columns for a clean 3-across display
                cols = st.columns(3)
                
                for i, item in enumerate(random_items):
                    with cols[i]:
                        st.success(f"**{item}**")
                
                st.write("") # Add a bit of vertical space
                
    else:
        st.error("Error: Could not find recommendation data for the calculated trope.")

# Run the page function
show_recommendation_page()