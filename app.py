import streamlit as st
from streamlit_folium import st_folium
import folium
import random

st.set_page_config(page_title="The Memory Challenge", page_icon="📍", layout="wide")

# 1. Locations with Direct Image Links (fixed for Imgur)
locations = [
    {
        "name": "Where we first met", 
        "coords": [54.88879, 23.92604], 
        "memory": "I'll never forget that white blouse you wore. 👚",
        "clue": "Let's start where it all began... Find the spot of our very first met! ☕",
        "image_url": "https://lh3.googleusercontent.com/p/AF1QipOhRntAB9mbmlZfHxsKAj9PE5ZDlmlIX2a0Pl2K=s680-w680-h510-rw" 
    },
    {
        "name": "Our First Date", 
        "coords": [56.24867, 24.69066], 
        "memory": "The trip was unplanned, but the conversation was perfect. 🍕",
        "clue": "Our first date! It was a bit of a drive, wasn't it? 🚗",
        "image_url": "https://i.imgur.com/g7VaplC.jpg"
    },
    {
        "name": "Our first trip together", 
        "coords": [56.94751, 24.10867], 
        "memory": "We planned a lot of things together, but Mintu had his own plans. 🥂",
        "clue": "Cross the border! Where did we head for our first big getaway? 🏰",
        "image_url": "https://i.imgur.com/aPpyF24.jpg"
    },
    {
        "name": "Our unexpected best restaurant", 
        "coords": [55.70679, 21.13755], 
        "memory": "We found it by random chance, but it will stick with us forever.❤️",
        "clue": "Hungry? Find that one place we stumbled upon that became our favorite. 🍝",
        "image_url": "https://i.imgur.com/vjZsUxL.jpg"
    }
]

# State Management
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'found' not in st.session_state:
    st.session_state.found = False

st.title("Memory Challenge: Guess the Spot! 🧩")
current_step = st.session_state.step

if current_step < len(locations):
    loc = locations[current_step]
    
    if not st.session_state.found:
        st.info(f"**Level {current_step + 1}:** {loc['clue']}")
    else:
        st.success(f"✨ Correct! You found: {loc['name']}")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(loc["image_url"], use_container_width=True)
        with col2:
            st.write(loc["memory"])
            if st.button("Next Challenge ➡️", use_container_width=True):
                st.session_state.step += 1
                st.session_state.found = False
                st.rerun()

    # Map setup
    m = folium.Map(location=loc["coords"], zoom_start=12)
    if st.session_state.found:
        folium.Marker(location=loc["coords"], icon=folium.Icon(color="red", icon="heart")).add_to(m)

    # Key is dynamic to force refresh after each level
    map_data = st_folium(m, width="100%", height=500, key=f"map_{current_step}")

    if map_data["last_clicked"] and not st.session_state.found:
        guess = [map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]]
        target = loc["coords"]
        if abs(guess[0] - target[0]) < 0.01 and abs(guess[1] - target[1]) < 0.01:
            st.session_state.found = True
            st.balloons()
            st.rerun()

else:
    # --- FINALE ---
    if current_step == len(locations):
        st.balloons()
        st.header("💌 You remembered everything!")
        st.write("We've traveled together and made so many plans. Let's make one more.")
        
        # Use a container to hold the buttons
        col_yes, col_no = st.columns(2)
        
        with col_yes:
            if st.button("YES! ❤️", use_container_width=True):
                st.snow()
                st.success("I love you! Best. Valentine's. Ever.")
                
        with col_no:
            # This version uses a more robust script to force the button to escape its box
            st.components.v1.html("""
                <style>
                    #runaway {
                        background-color: #ff4b4b;
                        color: white;
                        border: none;
                        padding: 12px 24px;
                        border-radius: 5px;
                        font-family: sans-serif;
                        cursor: pointer;
                        transition: 0.1s;
                        position: absolute;
                    }
                </style>
                <button id="runaway">No</button>
                <script>
                    const btn = document.getElementById('runaway');
                    // Function to move the button
                    const moveButton = () => {
                        btn.style.left = Math.random() * (window.innerWidth - 80) + 'px';
                        btn.style.top = Math.random() * (window.innerHeight - 40) + 'px';
                    };
                    
                    // Move on hover AND on click attempt
                    btn.addEventListener('mouseover', moveButton);
                    btn.addEventListener('click', (e) => {
                        e.preventDefault();
                        moveButton();
                        alert("Nice try! 'No' is out of order today. 😉");
                    });
                </script>
            """, height=300)

