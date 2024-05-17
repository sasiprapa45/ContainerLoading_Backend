from rest_framework import serializers
from .models import Cargoes, Container, TypeCargo,TypeContainer, Position,Project



# class CargoesChildSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cargoes
#         fields = ['name', 'type_cargo', 'weight', 'project_id']

class CargoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargoes
        fields = ['name', 'type_cargo', 'weight', 'project_id']
        
        
class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['type_container', 'project_id']

# class CargoesSerializer(serializers.ListSerializer):
#     child = CargoesChildSerializer()

#     def create(self, validated_data):
#         cargoes = [Cargoes(**item) for item in validated_data]
#         return Cargoes.objects.bulk_create(cargoes)

#     class Meta:
#         model = Cargoes
#         fields = ['name', 'type_cargo', 'weight', 'project_id']
        

class PositionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'
        
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields =  '__all__'