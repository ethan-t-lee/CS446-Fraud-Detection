import base64
import json
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

def score_transaction(txn):
    amount = float(txn.get("amount", 0))

    score = 0.02

    if amount > 800:
        score += 0.45
    elif amount > 300:
        score += 0.20

    score += random.uniform(0, 0.1)

    return round(min(score, 0.99), 4)

@app.post("/")
def receive_pubsub():
    envelope = request.get_json(silent=True)

    if not envelope:
        return jsonify({"error": "No JSON received"}), 400

    message = envelope.get("message", {})
    data = message.get("data")

    if not data:
        return jsonify({"error": "No Pub/Sub data found"}), 400

    decoded = base64.b64decode(data).decode("utf-8")
    transaction = json.loads(decoded)

    prediction = score_transaction(transaction)

    print({
        "transaction": transaction,
        "fraud_probability": prediction
    })

    return jsonify({
        "status": "processed",
        "transaction_id": transaction.get("transaction_id"),
        "fraud_probability": prediction
    }), 200

@app.get("/healthz")
def healthz():
    return "ok", 200
