from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = "brahim123"
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "YOUR_PAGE_TOKEN")

def get_ai_reply(user_message):
    return f"مرحبا! وصلتني رسالتك: '{user_message}' - راح نجاوبك قريبا 🙏"

def send_instagram_reply(recipient_id, text):
    url = f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {"recipient": {"id": recipient_id}, "message": {"text": text}}
    r = requests.post(url, json=payload)
    print("Send:", r.text)
    return r

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["GET"])
@app.route("/webhook/instagram-dm", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
@app.route("/webhook/instagram-dm", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return "OK", 200
    try:
        for entry in data.get("entry", []):
            for messaging in entry.get("messaging", []):
                sender_id = messaging.get("sender", {}).get("id")
                text = messaging.get("message", {}).get("text", "")
                if not text or not sender_id:
                    continue
                if messaging.get("message", {}).get("is_echo"):
                    continue
                reply = get_ai_reply(text)
                send_instagram_reply(sender_id, reply)
    except Exception as e:
        print(e)
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
