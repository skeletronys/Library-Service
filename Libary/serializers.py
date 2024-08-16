from rest_framework import serializers

from Libary.models import Book, Payment
from borrowings.models import Borrowing

from user.models import User


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_staff",
        )


class PaymentSerializer(serializers.ModelSerializer):
    borrowing = serializers.SlugRelatedField(
        queryset=Borrowing.objects.all(), slug_field="id"
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True, source="borrowing.user")

    class Meta:
        model = Payment
        fields = "__all__"
