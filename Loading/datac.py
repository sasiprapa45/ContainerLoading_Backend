
from .models import Cargoes, Container, Project

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
            'weight_pack': con.weight_pack,
            'type_container_id': con.type_container.id,
            'type_container': con.type_container.type,
            'height': con.type_container.height,
            'width': con.type_container.width,
            'length': con.type_container.length,
            'limit_weight': con.type_container.limit_weight,
        })
    return container_list

def get__project(project_id):
    project = Project.objects.get(pk=project_id)
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
    return data
