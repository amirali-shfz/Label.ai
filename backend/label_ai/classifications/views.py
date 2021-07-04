from rest_framework import generics

from .models import Classification
from .serializers import ClassificationSerializer


class ClassificationList(generics.ListAPIView):
    queryset = Classification.objects.raw("SELECT * FROM Classification")
    serializer_class = ClassificationSerializer