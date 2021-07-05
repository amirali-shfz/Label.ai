from django.db import connection
from django.http.response import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView

from label_ai import classifications, submissions

from .models import Submission
from .serializers import SubmissionSerializer


class SubmissionList(generics.ListAPIView):
    queryset = Submission.objects.raw("SELECT * FROM Submission")
    serializer_class = SubmissionSerializer


class SubmissionInsert(APIView):

    def post(self, request, format=None):
        correct_label = request.POST.get('correct_label')
        member_id = request.POST.get('member_id')
        class_id = request.POST.get('class_id')
        print(correct_label, member_id, class_id)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO submission(correct_label, member_id, class_id)
            VALUES(%s, %s, %s)
            """, [correct_label, member_id, class_id])

        # TODO: Fix response to be more informative and utilize fetchall()
        return JsonResponse({
            'vote': correct_label,
            'member_id': member_id,
            'class_id': class_id
        })

        
        