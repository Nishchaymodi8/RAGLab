from django.urls import path
from .views import health_check

from .views import *


urlpatterns = [
    path("health/", health_check, name="health"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/me/", MeView.as_view(), name="me"),
]