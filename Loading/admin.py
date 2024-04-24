from django.contrib import admin
from .models import TypeContainer, TypeCargo, Cargoes, Container, Project, Position
# Register your models here.
admin.site.register(TypeContainer)
admin.site.register(TypeCargo)
admin.site.register(Project)
