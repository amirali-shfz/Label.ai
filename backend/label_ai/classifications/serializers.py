from rest_framework import serializers

from .models import Classification

class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = (
            "class_id",
            "confidence",
            "true_count",
            "false_count",
            "pre_classified"
        )