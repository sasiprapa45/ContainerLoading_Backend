from django.urls import include, path
from rest_framework import routers
from . import views




# router = routers.DefaultRouter()
# router.register(r'cargoes', views.CargoesViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path("addProject/", views.AddProjectViewSet.as_view(), name="Project-view-create"),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('addProject/<str:project_name>/', views.AddProjectAPIView.as_view(), name='addProject'), # เพิ่ม URL สำหรับ API Endpoint
    path("addCargoes/", views.SaveCargoseAPIView.as_view(), name="Cargoes-view-create"),

]