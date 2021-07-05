from rest_framework import serializers

from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = (
            "submission_id",
            "correct_label",
            "member_id",
            "class_id",
        )
