from rest_framework import serializers

from Libary.models import Book, Borrowing, Payment

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


class UserFLNameSerializer(serializers.ModelSerializer):  # FL = first_name + last_name
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class BorrowingSerializer(serializers.ModelSerializer):
    Book = serializers.SlugRelatedField(queryset=Book.objects.all(), slug_field="name")
    User = UserFLNameSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"
