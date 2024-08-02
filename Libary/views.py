from rest_framework import viewsets

from Libary.models import Book, Borrowing, Payment
from Libary.serializers import (
    BookSerializer,
    CustomUserSerializer,
    BorrowingSerializer,
    PaymentSerializer,
)

from user.models import User


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(id=user.id)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
