from rest_framework import generics

from .models import Submission
from .serializers import SubmissionSerializer


class SubmissionList(generics.ListAPIView):
    queryset = Submission.objects.raw("SELECT * FROM Submission")
    serializer_class = SubmissionSerializer


