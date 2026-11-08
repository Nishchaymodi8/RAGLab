from django.urls import path

from .views import (
    DatasetDetailView,
    DatasetListCreateView,
)

urlpatterns = [
    path(
        "datasets/",
        DatasetListCreateView.as_view(),
        name="dataset-list-create",
    ),
    path(
        "datasets/<int:pk>/",
        DatasetDetailView.as_view(),
        name="dataset-detail",
    ),
]