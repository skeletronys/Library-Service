import os

from django.shortcuts import get_object_or_404
from django.urls.base import reverse
import stripe

from borrowings.models import Payment, Borrowing


stripe.api_key = os.getenv("API_KEY_STRIPE", "")


def create_stripe_session(request, borrowing_id):
    borrowing = get_object_or_404(Borrowing, id=borrowing_id)
    total_price = (
        borrowing.book.daily_fee
        * (borrowing.expected_return_date - borrowing.borrow).days
    )
    success_url = (
        request.build_absolute_uri(reverse("borrowings:payment-success"))
        + "?session_id={CHECKOUT_SESSION_ID}"
    )
    cancel_url = request.build_absolute_uri(reverse("borrowings:payment-cancel"))
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
        success_url=success_url,
        cancel_url=cancel_url,
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
