from rest_framework import serializers
from main.models import Subject


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "Subject"
        model = Subject
        fields = (
            'id',
            'name',
        )
