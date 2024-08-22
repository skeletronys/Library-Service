from django.urls import path, include
from rest_framework import routers

from Libary.views import (
    BookViewSet,
    CustomUserViewSet,
)

router = routers.DefaultRouter()
router.register("book", BookViewSet)
router.register("customer", CustomUserViewSet)

app_name = "Libary"

urlpatterns = [path("", include(router.urls))]
