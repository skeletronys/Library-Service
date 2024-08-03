from rest_framework import serializers

from Libary.models import Book

from borrowings.models import Borrowing

from user.models import User


class BorrowingSerializer(serializers.ModelSerializer):
    Book = serializers.SlugRelatedField(queryset=Book.objects.all(), slug_field="name")
    User = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Borrowing
        fields = "__all__"
