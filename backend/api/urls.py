from django.urls import path
from .views import health_check
from .views import *
from api.views import RetrievalView


urlpatterns = [
    path("health/", health_check, name="health"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("auth/google/", GoogleLoginView.as_view(), name="google-login"),
    path(
        "documents/",
        DocumentListCreateView.as_view(),
        name="documents",
    ),
    path(
    "retrieval/",
    RetrievalView.as_view(),
    name="retrieval",
),
    path("rag/", rag_view, name="rag"),
]