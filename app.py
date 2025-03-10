# app.py

from streamlit_autorefresh import st_autorefresh
import streamlit as st
import requests
import os
import base64
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
import logging

logging.basicConfig(level=logging.INFO)


st_autorefresh()

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
        unsafe_allow_html=True,
    )


st.title("IoT Lamp Control Panel")


def fetch_party_state():
    """Return (is_on, color) by calling the Flask server."""
    url = f"http://localhost:{api_port}/party-mode"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        is_on = data.get("state", False)
        return is_on
    except Exception as e:
        st.error(f"Error fetching party_mode: {e}")
        return False


def fetch_pray_state():
    """Return (is_on, color) by calling the Flask server."""
    url = f"http://localhost:{api_port}/pray-mode"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        is_on = data.get("state", False)
        return is_on
    except Exception as e:
        st.error(f"Error fetching party_mode: {e}")
        return False


def fetch_lamp_state(lamp_id):
    """Return (is_on, color) by calling the Flask server."""
    url = f"http://localhost:{api_port}/lamp/{lamp_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        is_on = data["state"] == "on"
        return is_on
    except Exception as e:
        st.error(f"Error fetching lamp {lamp_id}: {e}")
        return False


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


party_is_on = fetch_party_state()
if party_is_on:
    add_local_mp4_background("ramadan.mp4")

pray_mode = fetch_pray_state()
if pray_mode:
    add_local_mp4_background("ramadan.mp4")

lamp_ids = [1, 2, 3, 4]
cols = st.columns(len(lamp_ids))

for i, lamp_id in enumerate(lamp_ids):
    with cols[i]:
        st.subheader(f"Lamp {lamp_id}")

        # Fetch current state from the server
        is_on = fetch_lamp_state(lamp_id)

        # Show an icon and on/off status
        if is_on:
            st.markdown(
                "<h1 style='text-align: center;'>💡</h1>", unsafe_allow_html=True
            )
            st.write("Status: **ON**")
        else:
            st.markdown(
                "<h1 style='text-align: center;'>🔌</h1>", unsafe_allow_html=True
            )
            st.write("Status: **OFF**")
        if st.button(f"Toggle {lamp_id}"):
            toggle_lamp(lamp_id, not is_on)
            st.rerun()

# toggle_party_mode()

# Just a manual refresh button to re-fetch lamp states
if st.button("Refresh All"):
    st.rerun()
