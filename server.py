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
party_state = False 

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

@app.route("/party-mode", methods=["GET"])
def party_mode():
    return jsonify(
        {
            "state": party_state,
        }
    ), 200

@app.route("/party-mode/on", methods=["GET"])
def party_mode_on():
    global party_state
    party_state = True
    return jsonify(
        {
            "message": "Party mode turned on!",
            "state": party_state,
        }
    ), 200

@app.route("/party-mode/off", methods=["GET"])
def party_mode_off():
    global party_state
    party_state = False
    return jsonify(
        {
            "message": "Party mode turned off!",
            "state": party_state,
        }
    ), 200


if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 5000))
    app.run(port=port, debug=False)
