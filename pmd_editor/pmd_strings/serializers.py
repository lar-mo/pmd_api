from rest_framework import serializers

from .models import String

class StringSerializerv1(serializers.ModelSerializer):
    class Meta:
        model = String
        fields = ['id', 'location', 'updated', 'string']

class StringSerializerv2(serializers.ModelSerializer):
    class Meta:
        model = String
        fields = ['location', 'string']
