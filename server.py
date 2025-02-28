# server.py
from flask import Flask, jsonify
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Each lamp just has an "is_on" flag (no color)
lamp_states = {
    1: {"is_on": False},
    2: {"is_on": False},
    3: {"is_on": False},
    4: {"is_on": False},
}

@app.route("/lamp/<int:lamp_id>/on", methods=["GET"])
def lamp_on(lamp_id):
    if lamp_id in lamp_states:
        lamp_states[lamp_id]["is_on"] = True
        return jsonify({
            "lamp": lamp_id,
            "state": "on"
        }), 200
    else:
        return jsonify({"error": "Invalid lamp id"}), 404

@app.route("/lamp/<int:lamp_id>/off", methods=["GET"])
def lamp_off(lamp_id):
    if lamp_id in lamp_states:
        lamp_states[lamp_id]["is_on"] = False
        return jsonify({
            "lamp": lamp_id,
            "state": "off"
        }), 200
    else:
        return jsonify({"error": "Invalid lamp id"}), 404

@app.route("/lamp/<int:lamp_id>", methods=["GET"])
def get_lamp(lamp_id):
    if lamp_id in lamp_states:
        state = "on" if lamp_states[lamp_id]["is_on"] else "off"
        return jsonify({
            "lamp": lamp_id,
            "state": state
        }), 200
    else:
        return jsonify({"error": "Invalid lamp id"}), 404

# New endpoint: toggles all lamps at once (on->off, off->on).
@app.route("/party-mode", methods=["GET"])
def party_mode():
    for lamp_id in lamp_states:
        lamp_states[lamp_id]["is_on"] = not lamp_states[lamp_id]["is_on"]
    return jsonify({"message": "Party mode toggled all lamps!"}), 200

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 5000))
    app.run(port=port, debug=False)
