from rest_framework import serializers
from .models import Cargoes, Container, TypeCargo,TypeContainer, Position, Project, CustomUser
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'age', 'address', 'email')
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'age', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'age', 'address', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            age=validated_data.get('age'),
            address=validated_data.get('address'),
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data['username']
        password = data['password']

        if not username:
            raise serializers.ValidationError("Must include 'username'.")

        if not password:
            raise serializers.ValidationError("Must include 'password'.")

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                return user
            else:
                raise serializers.ValidationError("User account is disabled.")
        else:
            raise serializers.ValidationError("Invalid login credentials.")
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, data):
#         username = data.get('username')
#         password = data.get('password')

#         if username and password:
#             user = authenticate(request=self.context.get('request'), username=username, password=password)
#             if not user:
#                 raise serializers.ValidationError(_('Unable to log in with provided credentials.'), code='authorization')
#         else:
#             raise serializers.ValidationError(_('Must include "username" and "password".'), code='authorization')
#         data['user'] = user
#         return data

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