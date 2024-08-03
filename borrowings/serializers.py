from rest_framework import serializers

from Libary.models import Book

from borrowings.models import Borrowing

from user.models import User


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
