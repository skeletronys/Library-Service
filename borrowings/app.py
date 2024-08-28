import os
from flask import Flask, jsonify, redirect
import stripe

from borrowings.models import Payment

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


def create_stripe_session(borrowing):
    total_price = (
        borrowing.book.daily_fee
        * (borrowing.expected_return_date - borrowing.borrow).days
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": borrowing.book.name,
                    },
                    "unit_amount": int(total_price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://localhost:8000/success/",
        cancel_url="http://localhost:8000/cancel/",
    )
    days_borrowed = (borrowing.expected_return_date - borrowing.borrow).days

    payment = Payment.objects.create(
        borrowing=borrowing,
        status=Payment.StatusType.PENDING,
        type=Payment.Types.PAYMENT,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=days_borrowed * borrowing.book.daily_fee,
    )

    return payment


if __name__ == "__main__":
    app.run(port=4242)
