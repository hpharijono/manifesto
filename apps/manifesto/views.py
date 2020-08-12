from rest_framework import permissions, viewsets
from .models import Value, Principle
from .serializers import ValueSerializer, PrincipleSerializer


class ValueViewSet(viewsets.ModelViewSet):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class PrincipleViewSet(viewsets.ModelViewSet):
    queryset = Principle.objects.all()
    serializer_class = PrincipleSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
