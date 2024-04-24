from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CargoesSerializer
from .models import Cargoes

class CargoesViewSet(viewsets.ModelViewSet):
    queryset = Cargoes.objects.all().order_by('name')
    serializer_class = CargoesSerializer