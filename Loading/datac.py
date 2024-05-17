
from .models import Cargoes, Container

def get_cargoes_by_project_id(project_id):
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
    return cargoes_list

def get_container_by_project_id(project_id):
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
    return container_list

# def get_container_by_project_id(project_id):
#     url = f'http://127.0.0.1:8000/get_container_by_project_id/{project_id}/'  # แก้ตาม URL จริงของคุณ
#     response = requests.get(url)
#     if response.status_code == 200:
#         container_list = response.json().get('container_list')
#         return container_list
#     else:
#         print("Error:", response.status_code)
#         return []

# def get_cargoes_by_project_id(project_id):
#     url = f'http://127.0.0.1:8000/get_cargoes_by_project_id/{project_id}/'  # แก้ตาม URL จริงของคุณ
#     response = requests.get(url)
#     if response.status_code == 200:
#         cargoes_list = response.json().get('cargoes_list')
#         return cargoes_list
#     else:
#         print("Error:", response.status_code)
#         return []

# project_id = 21  # แก้เป็น project_id ที่ต้องการค้นหา cargoes
# cargoes_list = get_container_by_project_id(project_id)
# print(cargoes_list)

# cargoes_list=Cargoes(21)
# print(cargoes_list)
# # Containers()