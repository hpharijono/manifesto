from rest_framework import viewsets
from .models import Value, Principle
from .serializers import ValueSerializer, PrincipleSerializer


class ValueViewSet(viewsets.ModelViewSet):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer


class PrincipleViewSet(viewsets.ModelViewSet):
    queryset = Principle.objects.all()
    serializer_class = PrincipleSerializer