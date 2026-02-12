import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Our Journey", page_icon="📍", layout="wide")

# 1. Your locations with images added
locations = [
    {
        "name": "Where we first met", 
        "coords": [54.88879624710162, 23.9260471886652], 
        "memory": "I'll never forget that white blouse you wore. 👚",
        "clue": "Let's start where it all began... find the spot of our very first meeting! ☕",
        "image_url": "https://lh3.googleusercontent.com/p/AF1QipOhRntAB9mbmlZfHxsKAj9PE5ZDlmlIX2a0Pl2K=w426-h240-k-no" # REPLACE WITH REAL URL
    },
    {
        "name": "Our First Date", 
        "coords": [56.24867599469959, 24.69066371008891], 
        "memory": "The trip was unplanned, but the conversation was perfect. 🍕",
        "clue": "Our first official date! It was a bit of a drive, wasn't it? 🚗",
        "image_url": "https://maps.app.goo.gl/wcjGmqcaLh2Co4q48"
    },
    {
        "name": "Our first trip together", 
        "coords": [56.94751605162167, 24.108679117232104], 
        "memory": "We planned a lot of things together, but Mintu had his own plans. 🐶",
        "clue": "Cross the border! Where did we head for our first big getaway? 🏰",
        "image_url": "https://maps.app.goo.gl/A96h4vyepr3MMDw46"
    },
    {
        "name": "Our unexpected best restaurant", 
        "coords": [55.706792572044805, 21.137550531907657], 
        "memory": "We found it by random chance, but it will stick with us forever. ❤️",
        "clue": "Hungry? Find that one place we stumbled upon that became our favorite. 🍝",
        "image_url": "https://via.placeholder.com/400x300.png?text=Restaurant+Photo"
    }
]

# State Management
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'viewing_memory' not in st.session_state:
    st.session_state.viewing_memory = False

st.title("Our Love Map 🗺️")
current_step = st.session_state.step

# --- LOGIC: SHOW MEMORY CARD OR CLUE ---
if st.session_state.viewing_memory and current_step < len(locations):
    # This section appears ONLY when a marker is clicked
    loc = locations[current_step]
    st.markdown(f"### ✨ Memory Unlocked: {loc['name']}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(loc["image_url"], use_container_width=True)
    with col2:
        st.info(loc["memory"])
        if st.button("Continue our journey →", use_container_width=True):
            st.session_state.step += 1
            st.session_state.viewing_memory = False
            st.rerun()
            
elif current_step < len(locations):
    # Normal Clue View
    st.info(f"**Next Clue:** {locations[current_step]['clue']}")
    st.progress(current_step / len(locations))
else:
    st.success("🎉 You've unlocked all our memories!")

# --- MAP SECTION ---
# Auto-center
center_coords = locations[min(current_step, len(locations)-1)]["coords"]
m = folium.Map(location=center_coords, zoom_start=13, tiles="CartoDB positron")

# Markers
for i in range(current_step + 1):
    if i < len(locations):
        is_active = (i == current_step)
        folium.Marker(
            location=locations[i]["coords"],
            icon=folium.Icon(color="red" if is_active else "gray", icon="heart", prefix="fa")
        ).add_to(m)

# Capture Clicks
output = st_folium(m, width="100%", height=400)

if output["last_object_clicked"] and not st.session_state.viewing_memory:
    clicked = [output["last_object_clicked"]["lat"], output["last_object_clicked"]["lng"]]
    target = locations[current_step]["coords"]
    
    # Distance check
    if abs(clicked[0] - target[0]) < 0.005 and abs(clicked[1] - target[1]) < 0.005:
        st.session_state.viewing_memory = True
        st.rerun()

# --- FINALE ---
if current_step == len(locations):
    st.markdown("---")
    st.header("💌 One Final Question...")
    # Your specific text from the memories
    st.write("We've traveled together and made so many plans. Let's make one more.")
    if st.button("Will you be my Valentine? ❤️", use_container_width=True):
        st.balloons()
        st.snow()
        st.success("Yay! Can't wait for our next trip! ❤️")