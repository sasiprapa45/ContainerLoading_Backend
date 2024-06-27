from django.urls import include, path
from rest_framework import routers
from . import views




# router = routers.DefaultRouter()
# router.register(r'cargoes', views.CargoesViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    # path("addProject/", views.AddProjectViewSet.as_view(), name="Project-view-create"),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('addProject/', views.AddProjectAPIView.as_view(), name='addProject'), # เพิ่ม URL สำหรับ API Endpoint
    path("addCargoes/", views.SaveCargoseAPIView.as_view(), name="Cargoes-view-create"),
    path("addContainer/", views.SaveContainerAPIView.as_view(), name="Container-view-create"),
    # path('get_cargoes_by_project_id/<int:project_id>/', views.get_cargoes_by_project_id, name='get_cargoes_by_project_id'),
    # path('get_container_by_project_id/<int:project_id>/', views.get_container_by_project_id, name='get_container_by_project_id'),
    path('create_ga_algorithm/<int:project_id>/', views.CreateGaAPIView.as_view(), name='create_ga_algorithm_by_project_id'),
    path('positions/<int:project_id>/', views.GetPositionAPIView.get_positions_by_project, name='get_positions_by_project'),
    path('container_by_pid/<int:project_id>/', views.GetContainerAPIView.get_container_by_project, name='get_container_by_project'),
    path('project_by_pid/<int:project_id>/', views.GetProjectAPIView.get_project_by_pid, name='get_project_by_pid'),
    path('projects/<int:user_id>/', views.GetProject1APIView.as_view(), name='get_project'),
    path('deleteprojects/<int:project_id>/', views.DeleteProjectAPIView.as_view(), name='delete_project'),
    path('cargoes_by_pid/<int:project_id>/', views. GetCargoesAPIView.get_cargoes_by_project, name='get_cargoes_by_pid'),
    path('checkTypeCargoes/', views.CheckTypeCargoesAPIView.as_view(), name='get_cargoes_by_pid'),
    path('checkTypeContainer/', views.CheckTypeContainerAPIView.as_view(), name='get_container_by_pid'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('user/<int:id>/', views.UserDetailView.as_view(), name='user_detail'),
]