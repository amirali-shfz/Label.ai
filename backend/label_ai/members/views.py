from rest_framework import generics

from .models import Member
from .serializers import MemberSerializer


class MemberList(generics.ListAPIView):
    queryset = Member.objects.raw("SELECT * FROM Member")
    serializer_class = MemberSerializer