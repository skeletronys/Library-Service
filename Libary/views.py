from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from Libary.models import Book
from Libary.serializers import (
    BookSerializer,
    CustomUserSerializer,
)

from Libary.models import Customer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):

        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        return super(BookViewSet, self).get_permissions()


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Customer.objects.all()
        else:
            return Customer.objects.filter(id=user.id)
