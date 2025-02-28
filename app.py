# app.py

from streamlit_autorefresh import st_autorefresh
import streamlit as st
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

# Auto-refresh every 5000 milliseconds (5 seconds)
st_autorefresh(interval=5000, key="auto-refresh")

api_port = os.getenv("API_PORT", 5000)

def add_local_mp4_background(mp4_file: str):
    """
    Reads a local MP4 file, encodes it to base64,
    and embeds it as a <video> in the background.
    """
    with open(mp4_file, "rb") as f:
        data = f.read()
    encoded_mp4 = base64.b64encode(data).decode("utf-8")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: transparent !important;
        }}
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


def toggle_party_mode():
    url = f"http://localhost:{api_port}/party-mode"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        party_mode = data.get("party_mode", False)
        # Update the session state
        st.session_state["party_mode"] = party_mode
        st.success("Party mode toggled")
        return party_mode
    except Exception as e:
        st.error(f"Error toggling party mode: {e}")
        return False

# Initialize party_mode in session state
if "party_mode" not in st.session_state:
    st.session_state["party_mode"] = False

st.title("IoT Lamp Control Panel")

# If party mode is currently ON, embed the MP4 now
if st.session_state["party_mode"]:
    add_local_mp4_background("party.mp4")

# Party Mode Button
if st.button("Toggle Party Mode"):
    toggle_party_mode()

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
    """Turn the lamp on or off."""
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
        is_on, _ = fetch_lamp_state(lamp_id)
        if is_on:
            st.markdown("<h1 style='text-align: center;'>💡</h1>", unsafe_allow_html=True)
            st.write("Status: **ON**")
        else:
            st.markdown("<h1 style='text-align: center;'>🔌</h1>", unsafe_allow_html=True)
            st.write("Status: **OFF**")
        if st.button(f"Toggle {lamp_id}"):
            toggle_lamp(lamp_id, not is_on)
            st.rerun()

toggle_party_mode()

# Just a manual refresh button to re-fetch lamp states
if st.button("Refresh All"):
    st.rerun()
