from rest_framework import serializers
from .models import Cargoes, Container, TypeCargo,TypeContainer, Position,Project
class CargoesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cargoes
        fields =  '__all__'
        
class ContainerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Container
        fields =  '__all__'
        
class PositionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'
        
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields =  '__all__'