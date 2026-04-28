import base64
import json
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

def score_transaction(txn):
    amount = float(txn.get("amount", 0))

    # Base probability (most transactions are safe)
    score = 0.01

    if amount <= 50:
        score += 0.01   # very common → very low risk
    elif amount <= 100:
        score += 0.03   # common
    elif amount <= 200:
        score += 0.08   # less common
    elif amount <= 500:
        score += 0.25   # rare → higher risk
    elif amount <= 1000:
        score += 0.50   # very rare → high risk
    else:
        score += 0.70   # extreme outlier → very high risk

    # add small randomness for realism
    import random
    score += random.uniform(0, 0.05)

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

    print(f"Processed transaction {transaction.get('transaction_id')} with fraud probability {prediction}")

    # Add BigQuery inserts here







    return jsonify({
        "status": "processed",
        "transaction_id": transaction.get("transaction_id"),
        "fraud_probability": prediction
    }), 200

@app.get("/healthz")
def healthz():
    return "ok", 200
