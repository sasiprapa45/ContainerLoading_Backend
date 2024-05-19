from urllib import response
from django.shortcuts import render
from rest_framework import viewsets,generics, status
from rest_framework.response import Response
from .serializers import CargoesSerializer, ProjectSerializer, ContainerSerializer
from .models import Cargoes, Project, Container, Position, TypeContainer, TypeCargo
from rest_framework.views import APIView
# from .algorithm.population import Population
from django.http import JsonResponse
from .population import Population
class AddProjectViewSet(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
# class AddProjectAPIView(APIView):
#     def get(self, request, project_name, *args, **kwargs):
#         try:
#             project = Project.objects.get(name=project_name) # ค้นหาโปรเจกต์จากชื่อ
#             return Response({'id': project.id}, status=200) # ส่ง ID กลับมาให้ Angular
#         except Project.DoesNotExist:
#             return Response({'error': 'Project not found'}, status=404)
        
class AddProjectAPIView(APIView):
     def get(self, request, project_name, *args, **kwargs):
        try:
            # สร้างหรือรับข้อมูลโปรเจกต์จากชื่อ
            if Project.objects.filter(name=project_name).exists():
                return Response({'error': 'Project with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            project, created = Project.objects.get_or_create(
                name=project_name,
                defaults={
                    'cargoes_qty': 0,
                    'cargoes_packed': 0,
                    'container_qty': 0,
                    'container_used': 0,
                    'fitness': 0.0,
                }
            )
            return Response({'id': project.pk}, status=status.HTTP_200_OK) # ส่ง ID กลับมาให้ Angular
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        
class GetProjectAPIView(APIView):
    def get_project(self, request, *args, **kwargs):
        projectall = Project.objects
        data = [{
            'id': project.pk,
            'name': project.name,
            'cargoes_qty': project.cargoes_qty,
            'cargoes_packed': project.cargoes_packed,
            'container_qty': project.container_qty,
            'container_used': project.container_used,
            'fitness': project.fitness,
            } for project in projectall]
        return JsonResponse(data, safe=False)
        
    def get_project_by_pid(request, project_id):
        projectaid = Project.objects.filter(id=project_id)
        data = [{
            'id': project.pk,
            'name': project.name,
            'cargoes_qty': project.cargoes_qty,
            'cargoes_packed': project.cargoes_packed,
            'container_qty': project.container_qty,
            'container_used': project.container_used,
            'fitness': project.fitness,
            }for project in projectaid]
        return JsonResponse(data, safe=False)
    
        
        
class SaveCargoseAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CargoesSerializer(data=request.data, many=True)  # ใช้ many=True เพื่อรับข้อมูลหลายรายการ
        if serializer.is_valid():
            serializer.save()  # บันทึกข้อมูลลงในฐานข้อมูล
            return Response({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
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
            result,cargoes_qty,cargoes_packed,container_qty,container_used,fitness = Population(project_id)
            
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
            'type_container_id': container.type_container.id,
            'type_container_name': container.type_container.type,
            'height': container.type_container.height,
            'width': container.type_container.width,
            'length': container.type_container.length,
            } for container in containers]
        return JsonResponse(data, safe=False)
    def get_type_container(request, project_id):
        type_containers = TypeContainer.objects
        data = [{
            'id': t_c.pk,
            'type_name': t_c.type,
            'height': t_c.height,
            'width': t_c.width,
            'length': t_c.length,
            } for t_c in type_containers]
        return JsonResponse(data, safe=False)
    
    
class GetCargoesAPIView(APIView):     
    def get_cargoes_by_project(request, project_id):
        cargoes = Cargoes.objects.filter(project_id=project_id).select_related('type_cargo')
        data = [{
            'id': car.pk,
            'project_id': car.project_id.id,
            'type_container_id': car.type_cargo.id,
            'type_container_name': car.type_cargo.type,
            'height': car.type_cargo.height,
            'width': car.type_cargo.width,
            'length': car.type_cargo.length,
            } for car in cargoes]
        return JsonResponse(data, safe=False)
    def get_type_cargoes(request, project_id):
        type_cargoes = TypeCargo.objects
        data = [{
            'id': t_c.pk,
            'type_name': t_c.type,
            'height': t_c.height,
            'width': t_c.width,
            'length': t_c.length,
            } for t_c in type_cargoes]
        return JsonResponse(data, safe=False)
        

def get_cargoes_by_project_id(request, project_id):
    cargoes_with_type = Cargoes.objects.filter(project_id=project_id).select_related('type_cargo')
    
    cargoes_list = []
    for cargo in cargoes_with_type:
        cargoes_list.append({
            'id': cargo.id,
            'name': cargo.name,
            'weight': cargo.weight,
            'project_id': cargo.project_id.id,  # เปลี่ยน project_id เป็น ID ของโปรเจกต์
            'type_cargo_id': cargo.type_cargo.id,
            'type_cargo': cargo.type_cargo.type,
            'height': cargo.type_cargo.height,
            'width': cargo.type_cargo.width,
            'length': cargo.type_cargo.length,
        })
    
    return JsonResponse({'cargoes_list': cargoes_list})
    
def get_container_by_project_id(request, project_id):
    container_with_type = Container.objects.filter(project_id=project_id).select_related('type_container')
    
    container_list = []
    for con in container_with_type:
        container_list.append({
            'id': con.id,
            'project_id': con.project_id.id,  # เปลี่ยน project_id เป็น ID ของโปรเจกต์
            'type_container_id': con.type_container.id,
            'type_container': con.type_container.type,
            'height': con.type_container.height,
            'width': con.type_container.width,
            'length': con.type_container.length,
            'limit_weight': con.type_container.limit_weight,
        })
    
    return JsonResponse({'container_list': container_list})


# class SaveCargoseAPIView(generics.ListCreateAPIView):
#     queryset = Cargoes.objects.all()
#     serializer_class = CargoesSerializer

    