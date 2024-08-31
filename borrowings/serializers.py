import datetime
import stripe

from decimal import Decimal
from django.urls.base import reverse
from rest_framework import serializers
from Libary.models import Book
from Libary_Service import settings
from borrowings.models import Borrowing, Payment


class PaymentSerializer(serializers.ModelSerializer):
    borrowing = serializers.SlugRelatedField(
        queryset=Borrowing.objects.all(), slug_field="id"
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True, source="borrowing.user")

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = [
            "status",
            "type",
            "session_url",
            "session_id",
            "money_to_pay",
        ]

    def create(self, validated_data):
        borrowing = validated_data.get("borrowing")
        request = self.context.get("request")
        success_url = (
            request.build_absolute_uri(reverse("borrowings:payment-success"))
            + "?session_id={CHECKOUT_SESSION_ID}"
        )
        cancel_url = request.build_absolute_uri(reverse("borrowings:payment-cancel"))

        stripe.api_key = settings.STRIPE_API_KEY
        days_borrowed = (borrowing.expected_return_date - borrowing.borrow).days

        if borrowing.expected_return_date < datetime.date.today():
            overdue_days = (datetime.date.today() - borrowing.expected_return_date).days
            fine_amount = overdue_days * Decimal(borrowing.book.daily_fee) * Decimal(
                settings.FINE_MULTIPLIER
            ) + Decimal(days_borrowed) * Decimal(borrowing.book.daily_fee)
            total_price = fine_amount
            payment_type = Payment.Types.FINE
        else:
            total_price = Decimal(days_borrowed) * Decimal(borrowing.book.daily_fee)
            payment_type = Payment.Types.PAYMENT

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

        payment = Payment.objects.create(
            borrowing=borrowing,
            status=Payment.StatusType.PENDING,
            type=payment_type,
            session_url=session.url,
            session_id=session.id,
            money_to_pay=int(total_price),
        )

        return payment


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(queryset=Book.objects.all(), slug_field="name")
    user = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = "__all__"
        read_only_fields = ["user", "actual_return_date"]

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def validate(self, data):
        if data["expected_return_date"] < data["borrow"]:
            raise serializers.ValidationError(
                "Expected return date cannot be before borrow date."
            )
        if "actual_return_date" in data and data["actual_return_date"] is not None:
            if data["actual_return_date"] < data["borrow"]:
                raise serializers.ValidationError(
                    "Actual return date cannot be before borrow date."
                )
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user:
            raise serializers.ValidationError("User is not authenticated.")

        book = validated_data.get("book")
        if not book:
            raise serializers.ValidationError("Book is required.")

        if book.inventory >= 1:
            book.inventory -= 1
            book.save()
        else:
            raise serializers.ValidationError("This book is currently out of stock.")

        borrowing = Borrowing.objects.create(
            book=book,
            user=request.user,
            borrow=validated_data["borrow"],
            expected_return_date=validated_data["expected_return_date"],
        )

        return borrowing

    def return_borrowing(self, instance):
        if instance.actual_return_date is not None:
            raise serializers.ValidationError(
                "This borrowing has already been returned."
            )

        instance.actual_return_date = datetime.date.today()

        if instance.actual_return_date > instance.expected_return_date:
            overdue_days = (
                instance.actual_return_date - instance.expected_return_date
            ).days
            fine_amount = (
                overdue_days * instance.book.daily_fee * settings.FINE_MULTIPLIER
            )

            Payment.objects.create(
                borrowing=instance,
                status=Payment.StatusType.PENDING,
                type=Payment.Types.FINE,
                money_to_pay=fine_amount,
            )

        instance.book.inventory += 1
        instance.book.save()

        instance.save()
        return instance
