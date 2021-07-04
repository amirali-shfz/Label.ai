from rest_framework import generics

from .models import Image
from .serializers import ImageSerializer


class ImageList(generics.ListAPIView):
    queryset = Image.objects.raw("SELECT * FROM Image")
    serializer_class = ImageSerializer
