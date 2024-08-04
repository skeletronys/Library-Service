from django.urls import path, include
from rest_framework import routers

from Libary.views import (
    BookViewSet,
    CustomUserViewSet,
    PaymentViewSet,
)

router = routers.DefaultRouter()
router.register("book", BookViewSet)
router.register("customer", CustomUserViewSet)
router.register("payment", PaymentViewSet)

app_name = "Libary"

urlpatterns = [path("", include(router.urls))]
