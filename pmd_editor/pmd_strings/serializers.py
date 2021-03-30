from rest_framework import serializers

from .models import String

class StringSerializerv1(serializers.ModelSerializer):
    string = serializers.CharField(source='string_en') # for backwards compatibility
    class Meta:
        model = String
        fields = ['id', 'location', 'updated', 'string']

class StringSerializerv2(serializers.ModelSerializer):
    string = serializers.CharField(source='string_en') # for backwards compatibility
    class Meta:
        model = String
        fields = ['location', 'string']

class StringSerializerv3(serializers.ModelSerializer):
    class Meta:
        model = String
        fields = ['location', 'string_en', 'string_es', 'string_fr', 'string_de']
