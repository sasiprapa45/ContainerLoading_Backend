from urllib import response
from django.shortcuts import render
from rest_framework import viewsets,generics, status
from rest_framework.response import Response
from .serializers import CargoesSerializer, ProjectSerializer
from .models import Cargoes, Project
from rest_framework.views import APIView


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
            project, created = Project.objects.get_or_create(name=project_name)
            return Response({'id': project.pk}, status=status.HTTP_200_OK) # ส่ง ID กลับมาให้ Angular
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

# class SaveCargoseAPIView(generics.ListCreateAPIView):
#     queryset = Cargoes.objects.all()
#     serializer_class = CargoesSerializer

    