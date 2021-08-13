from rest_framework import serializers

from .models import Classification

class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = (
            "class_id",
            "img_id",
            "label_id",
            "pre_classified",
            "total_votes",
            "confidence"
        )