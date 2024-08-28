import datetime

from rest_framework import serializers
from Libary.models import Book
from borrowings.models import Borrowing, Payment


class PaymentSerializer(serializers.ModelSerializer):
    borrowing = serializers.SlugRelatedField(
        queryset=Borrowing.objects.all(), slug_field="id"
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True, source="borrowing.user")

    class Meta:
        model = Payment
        fields = "__all__"


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(queryset=Book.objects.all(), slug_field="name")
    user = serializers.SerializerMethodField()
    payments = PaymentSerializer(many=True, read_only=True)

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

        instance.book.inventory += 1
        instance.book.save()

        instance.save()
        return instance
