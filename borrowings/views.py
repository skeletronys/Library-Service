from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, views
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


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
        serializer.save(user=self.request.user)


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
