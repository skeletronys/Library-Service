from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, views
from rest_framework.response import Response

from borrowings.app import create_stripe_session
from borrowings.models import Borrowing, Payment
from borrowings.serializers import BorrowingSerializer, PaymentSerializer

from telegramBot import send_telegram_message


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Borrowing.objects.all()

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(actual_return_date__isnull=False)

        user_id = self.request.query_params.get("user_id")
        if user.is_staff and user_id is not None:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def perform_create(self, serializer):
        borrowing = serializer.save(user=self.request.user)
        create_stripe_session(borrowing)
        message = (
            f"New borrowing created!\n"
            f"Id borrowing: {borrowing.id}\n"
            f"Book: {borrowing.book.name}\n"
            f"User: {borrowing.user.first_name} {borrowing.user.last_name}\n"
            f"Borrow date: {borrowing.borrow}\n"
            f"Expected return date: {borrowing.expected_return_date}"
        )
        send_telegram_message(message)


class ReturnBorrowingView(views.APIView):
    def post(self, request, pk):
        try:
            borrowing = Borrowing.objects.get(pk=pk)
        except Borrowing.DoesNotExist:
            return Response(
                {"detail": "Borrowing not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = BorrowingSerializer()
        try:
            serializer.return_borrowing(borrowing)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"detail": "Borrowing returned successfully."}, status=status.HTTP_200_OK
        )


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return self.queryset.filter(borrowing__user=user)
        return self.queryset
