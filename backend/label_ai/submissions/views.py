from django.db import connection
from django.http.response import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView

from label_ai import submissions

from .models import Submission
from .serializers import SubmissionSerializer

from json import loads

class SubmissionList(generics.ListAPIView):
    queryset = Submission.objects.raw("SELECT * FROM Submission")
    serializer_class = SubmissionSerializer


class SubmissionInsert(APIView):
    def post(self, request, format=None):
        body = loads(request.body.decode('utf-8'))
        correct_label = body['correct_label']
        member_id = body['member_id']
        class_id = body['class_id']
        cursor = connection.cursor()


        if correct_label == 'idk':
            correct_label = 'NULL'

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

        
        