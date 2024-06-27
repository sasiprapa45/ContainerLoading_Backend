from urllib import response
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets,generics, status,permissions
from rest_framework.response import Response
from .serializers import CargoesSerializer, ProjectSerializer, ContainerSerializer, RegisterSerializer, LoginSerializer, CustomUserSerializer, RegisterSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from .models import Cargoes, Project, Container, Position, TypeContainer, TypeCargo, CustomUser
from rest_framework.views import APIView
# from .algorithm.population import Population
from django.http import JsonResponse
from .population import Population
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny



class AddProjectViewSet(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    

class AddProjectAPIView(APIView):
     def post(self, request, *args, **kwargs):
        project_name = request.data.get('projectName')
        check_weight = request.data.get('checkWeight')
        user_id = request.data.get('userId')

        if not project_name:
            return Response({'error': 'Project name is required'}, status=status.HTTP_400_BAD_REQUEST)

        if Project.objects.filter(name=project_name, user=user_id).exists():
            return Response({'error': 'Project with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(pk=user_id)  # ตรวจสอบว่ามี User ID นี้หรือไม่
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        project = Project.objects.create(
            name=project_name,
            cargoes_qty=0,
            cargoes_packed=0,
            container_qty=0,
            container_used=0,
            fitness=0.0,
            weight_check=check_weight,
            user= user
        )
        return Response({'id': project.pk}, status=status.HTTP_201_CREATED)
        
class GetProjectAPIView(APIView):
      
    def get_project_by_pid(request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        data = {
            'id': project.pk,
            'name': project.name,
            'cargoes_qty': project.cargoes_qty,
            'cargoes_packed': project.cargoes_packed,
            'container_qty': project.container_qty,
            'container_used': project.container_used,
            'fitness': project.fitness,
            'weight_check': project.weight_check,
        }
        return JsonResponse(data)
    
class GetProject1APIView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id is None:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        projectall = Project.objects.filter(user_id=user_id)
        data = [{
            'id': project.pk,
            'name': project.name,
            'cargoes_qty': project.cargoes_qty,
            'cargoes_packed': project.cargoes_packed,
            'container_qty': project.container_qty,
            'container_used': project.container_used,
            'fitness': project.fitness,
            'user': project.user.id,
            'username': project.user.username,
        } for project in projectall]
        return Response(data, status=status.HTTP_200_OK)
    
class DeleteProjectAPIView(APIView):
    def delete(self, request, project_id, *args, **kwargs):
        try:
            project = Project.objects.get(pk=project_id)
            project.delete()  # This will cascade delete cargoes and positions if on_delete is set to CASCADE
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        
class SaveCargoseAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CargoesSerializer(data=request.data, many=True)  # ใช้ many=True เพื่อรับข้อมูลหลายรายการ
        if serializer.is_valid():
            serializer.save()  # บันทึกข้อมูลลงในฐานข้อมูล
            return Response({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CheckTypeCargoesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        type_cargoes = request.data.get('typeCargoes', [])
        invalid_type_cargoes = [tc for tc in type_cargoes if not TypeCargo.objects.filter(pk=tc).exists()]

        if invalid_type_cargoes:
            return Response({'isValid': False, 'invalidTypeCargoes': invalid_type_cargoes}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'isValid': True}, status=status.HTTP_200_OK)
    
class CheckTypeContainerAPIView(APIView):
    def post(self, request, *args, **kwargs):
        type_container = request.data.get('typeContainer', [])
        invalid_type_container  = [tc for tc in type_container  if not TypeContainer.objects.filter(pk=tc).exists()]

        if invalid_type_container:
            return Response({'isValid': False, 'invalidTypeContainer': invalid_type_container}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'isValid': True}, status=status.HTTP_200_OK)
class SaveContainerAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ContainerSerializer(data=request.data, many=True)  # ใช้ many=True เพื่อรับข้อมูลหลายรายการ
        if serializer.is_valid():
            serializer.save()  # บันทึกข้อมูลลงในฐานข้อมูล
            return Response({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class CreateGaAPIView(APIView):
     def get(self, request, project_id, *args, **kwargs):
        try:
            # ทำการคำนวณด้วยอัลกอริทึม Population และได้ผลลัพธ์ result
            result,cargoes_qty,cargoes_packed,container_qty,container_used,fitness,con_weight = Population(project_id)
            
            # บันทึกผลลัพธ์ลงในฐานข้อมูล
            for item in result:
                # สร้าง Position และบันทึกลงในฐานข้อมูล
                print(item)
                position = Position.objects.create(
                    X=item.x,
                    Y=item.y,
                    Z=item.z,
                    cargoes_id=Cargoes.objects.get(pk=item.cargoes_id),
                    container_id=Container.objects.get(pk=item.container_id),
                )
                position.save()
                
            for con in con_weight:
                print(con)
                container_update = Container.objects.get(pk=con.container_id)
                container_update.weight_pack = con.weight_pack
                    
                container_update.save()
            
            project = Project.objects.get(pk=project_id)
            project.cargoes_qty = cargoes_qty
            project.cargoes_packed = cargoes_packed
            project.container_qty = container_qty
            project.container_used = container_used
            project.fitness = fitness
            project.save()
            
            return JsonResponse({'message': 'Result saved successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
class GetPositionAPIView(APIView):
    def get_positions_by_project(request, project_id):
        cargoes = Cargoes.objects.filter(project_id=project_id)
        positions = Position.objects.filter(cargoes_id__in=cargoes)
        data = [{
            'id': position.pk,
            'X': position.X,
            'Y': position.Y,
            'Z': position.Z,
            'cargoes_id': position.cargoes_id.id,
            'name': position.cargoes_id.name,
            'weight': position.cargoes_id.weight,
            'project_id': position.cargoes_id.project_id.id,
            'type_cargo_id': position.cargoes_id.type_cargo.id,
            'height': position.cargoes_id.type_cargo.height,
            'width': position.cargoes_id.type_cargo.width,
            'length': position.cargoes_id.type_cargo.length,
            'color': position.cargoes_id.type_cargo.color,
            'container_id': position.container_id.id
            } for position in positions]
        return JsonResponse(data, safe=False)
    
class GetContainerAPIView(APIView):     
    def get_container_by_project(request, project_id):
        containers = Container.objects.filter(project_id=project_id).select_related('type_container')
        data = [{
            'id': container.pk,
            'project_id': container.project_id.id,
            'packing_weight': container.weight_pack,
            'type_container_id': container.type_container.id,
            'limit_weight': container.type_container.limit_weight,
            'type_container_name': container.type_container.type,
            'height': container.type_container.height,
            'width': container.type_container.width,
            'length': container.type_container.length,
            } for container in containers]
        return JsonResponse(data, safe=False)
 
    
class GetCargoesAPIView(APIView):     
    def get_cargoes_by_project(request, project_id):
        cargoes = Cargoes.objects.filter(project_id=project_id).select_related('type_cargo')
        data = [{
            'id': car.pk,
            'name': car.name,
            'project_id': car.project_id.id,
            'type_cargo': car.type_cargo.id,
            'type_cargo_name': car.type_cargo.type,
            'height': car.type_cargo.height,
            'width': car.type_cargo.width,
            'length': car.type_cargo.length,
            } for car in cargoes]
        return JsonResponse(data, safe=False)
        
        
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get(self, request, id, *args, **kwargs):
        try:
            user = CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'No CustomUser matches the given query.'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'address': user.address,
        }
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({'id': user.id, 'token': token.key})

    