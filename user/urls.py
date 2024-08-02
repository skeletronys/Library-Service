from django.urls import path, include
from rest_framework import routers

from user.views import UserViewSet

router = routers.DefaultRouter()
router.register("user", UserViewSet)


app_name = "user"

urlpatterns = [path("", include(router.urls))]
