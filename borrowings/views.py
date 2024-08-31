import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, views
from rest_framework.response import Response

import stripe

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

        if borrowing.actual_return_date is not None:
            return Response(
                {"detail": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = datetime.date.today()

        borrowing.book.inventory += 1
        borrowing.book.save()

        borrowing.save()

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


class PaymentSuccessView(View):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        if not session_id:
            return HttpResponse("Session ID not provided.", status=400)

        session = stripe.checkout.Session.retrieve(session_id)
        payment = get_object_or_404(Payment, session_id=session.id)

        if session.payment_status == "paid":
            payment.status = Payment.StatusType.PAID
            payment.save()
            return HttpResponse("Payment was successful!", status=200)
        else:
            return HttpResponse("Payment was not successful.", status=400)


class PaymentCancelView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(
            "Payment was canceled. You can try again later.", status=200
        )
