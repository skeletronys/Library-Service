from django.urls import path, include
from rest_framework import routers

from Libary.views import (
    BookViewSet,
    CustomUserViewSet,
    BorrowingViewSet,
    PaymentViewSet,
)

router = routers.DefaultRouter()
router.register("book", BookViewSet)
router.register("customer", CustomUserViewSet)
router.register("brrowing", BorrowingViewSet)
router.register("payment", PaymentViewSet)

app_name = "Libary"

urlpatterns = [path("", include(router.urls))]
