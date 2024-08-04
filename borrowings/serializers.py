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

    def create(self, validated_data):
        book = validated_data.get("Book")
        if book.inventory >= 1:
            book.inventory -= 1
            book.save()
        else:
            raise serializers.ValidationError("This book is currently out of stock.")

        borrowing = Borrowing.objects.create(
            Book=book,
            User=self.context["request"].user,
            Borrow=validated_data["Borrow"],
            Expected_return_date=validated_data["Expected_return_date"],
        )

        return borrowing
