import os
from flask import Flask, jsonify, redirect
import stripe

app = Flask(__name__)

stripe.api_key = os.getenv("API_KEY_STRIPE", "")


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": "price_1PrqIRP12cEirxdWiV6Mwact",
                    "quantity": 10,
                }
            ],
            mode="payment",
            success_url="http://localhost:4242/success",
            cancel_url="http://localhost:4242/cancel",
        )
        return jsonify({"session_url": session.url, "session_id": session.id}), 200
    except Exception as e:
        return jsonify(error=str(e)), 403


if __name__ == "__main__":
    app.run(port=4242)
