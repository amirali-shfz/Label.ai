from rest_framework import serializers

from .models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = (
            "member_id",
            "username",
            "password",
            "trust",
            "name",
            "is_admin"
        )