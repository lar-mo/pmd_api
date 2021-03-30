from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_api_key.permissions import HasAPIKey

from .models import String
from .serializers import StringSerializerv1, StringSerializerv2, StringSerializerv3

class StringViewSetv1(viewsets.ModelViewSet):
    queryset = String.objects.order_by('-updated')
    serializer_class = StringSerializerv1
    permission_classes = [IsAuthenticatedOrReadOnly]

class StringViewSetv2(viewsets.ModelViewSet):
    queryset = String.objects.order_by('id')
    serializer_class = StringSerializerv2
    permission_classes = [HasAPIKey & IsAuthenticatedOrReadOnly]

class StringViewSetv3(viewsets.ModelViewSet):
    queryset = String.objects.order_by('id')
    serializer_class = StringSerializerv3
    permission_classes = [HasAPIKey & IsAuthenticatedOrReadOnly]
