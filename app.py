import streamlit as st
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

def add_local_mp4_background(mp4_file: str):
    """
    Reads a local MP4 file and encodes it to a base64 string,
    then embeds it as a <video> in the Streamlit background.
    """
    with open(mp4_file, "rb") as f:
        data = f.read()
    encoded_mp4 = base64.b64encode(data).decode("utf-8")
    
    st.markdown(
        f"""
        <style>
        /* Make the main container transparent so the video shows through. */
        .stApp {{
            background-color: transparent !important;
        }}
        
        /* Create a full-screen fixed background video. */
        .background-video {{
            position: fixed;
            top: 0;
            left: 0;
            min-width: 100%;
            min-height: 100%;
            z-index: -1;
            object-fit: cover; /* Crop/cover to fill screen area. */
        }}
        </style>
        
        <video autoplay loop muted playsinline class="background-video">
            <source src="data:video/mp4;base64,{encoded_mp4}" type="video/mp4">
        </video>
        """,
        unsafe_allow_html=True
    )

st.title("IoT Lamp Control Panel")

# --- Party Mode Checkbox ---
party_mode = st.checkbox("Party Mode")
if party_mode:
    add_local_mp4_background("party.mp4")  # Adjust filename/path if needed

api_port = os.getenv("API_PORT", 5000)

def fetch_lamp_state(lamp_id):
    """Return (is_on, color) by calling the Flask server."""
    url = f"http://localhost:{api_port}/lamp/{lamp_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        is_on = (data["state"] == "on")
        color = data.get("color", "#FFFFFF")
        return is_on, color
    except Exception as e:
        st.error(f"Error fetching lamp {lamp_id}: {e}")
        return False, "#FFFFFF"

def toggle_lamp(lamp_id, turn_on: bool):
    """Turn the lamp on or off, returning the new color."""
    action = "on" if turn_on else "off"
    url = f"http://localhost:{api_port}/lamp/{lamp_id}/{action}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("color", "#FFFFFF")
    except Exception as e:
        st.error(f"Error toggling lamp {lamp_id}: {e}")
        return "#FFFFFF"

lamp_ids = [1, 2, 3, 4]

cols = st.columns(len(lamp_ids))
for i, lamp_id in enumerate(lamp_ids):
    with cols[i]:
        st.subheader(f"Lamp {lamp_id}")

        # Fetch current state from the server
        is_on, _ = fetch_lamp_state(lamp_id)

        # Show an icon and on/off status
        if is_on:
            st.markdown("<h1 style='text-align: center;'>💡</h1>", unsafe_allow_html=True)
            st.write("Status: **ON**")
        else:
            st.markdown("<h1 style='text-align: center;'>🔌</h1>", unsafe_allow_html=True)
            st.write("Status: **OFF**")

        # Toggle button
        if st.button(f"Toggle {lamp_id}"):
            toggle_lamp(lamp_id, not is_on)
            # Force a re-run to refresh the UI
            st.rerun()

# Optional refresh-all button
if st.button("Refresh All"):
    st.rerun()
