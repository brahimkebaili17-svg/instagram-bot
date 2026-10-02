from flask import Flask, request
import os, requests

app = Flask(__name__)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "brahim123")
PAGE_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get('object') == 'instagram':
        for entry in data.get('entry', []):
            for msg in entry.get('messaging', []):
                if 'message' in msg:
                    sender = msg['sender']['id']
                    text = msg['message'].get('text','')
                    if text:
                        requests.post(f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_TOKEN}",
                        json={"recipient":{"id":sender},"message":{"text":"سلام! 👋 تم استلام: "+text}})
    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)