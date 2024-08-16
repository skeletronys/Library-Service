from django.urls import path, include
from rest_framework import routers

from borrowings.views import BorrowingViewSet, ReturnBorrowingView

router = routers.DefaultRouter()
router.register("borrowings", BorrowingViewSet)


app_name = "borrowings"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "borrowings/<int:pk>/return/",
        ReturnBorrowingView.as_view(),
        name="return-borrowing",
    ),
]
