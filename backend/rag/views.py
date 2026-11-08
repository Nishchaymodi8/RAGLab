from rest_framework import generics

from .models import Dataset
from .serializers import DatasetSerializer


class DatasetListCreateView(generics.ListCreateAPIView):
    queryset = Dataset.objects.all().order_by("-created_at")
    serializer_class = DatasetSerializer


class DatasetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer