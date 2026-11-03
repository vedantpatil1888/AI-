"""Flask backend for the College Chatbot.

Run:  python app.py   then open http://127.0.0.1:5000
"""
from flask import Flask, jsonify, render_template, request

from chatbot_engine import ChatBot

app = Flask(__name__)
bot = ChatBot()


@app.route("/")
def home():
    return render_template("index.html", college_name=bot.data["college_name"])


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Message is empty."}), 400
    if len(message) > 300:
        return jsonify({"error": "Message is too long (max 300 characters)."}), 400
    return jsonify(bot.reply(message))


@app.route("/health")
def health():
    return jsonify({"status": "ok", "intents": len(bot.responses)})


if __name__ == "__main__":
    app.run(debug=True)
