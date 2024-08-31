from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenVerifyView,
)

from Libary.views import (
    BookViewSet,
    CustomUserViewSet,
)

router = routers.DefaultRouter()
router.register("book", BookViewSet)
router.register("customer", CustomUserViewSet)

app_name = "Libary"

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
