from rest_framework import generics

from .models import Label
from .serializers import LabelSerializer


class LabelList(generics.ListAPIView):
    queryset = Label.objects.raw("SELECT * FROM Label")
    serializer_class = LabelSerializer