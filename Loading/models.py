from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class TypeContainer(models.Model):
    type = models.CharField(max_length=20)
    height = models.IntegerField()
    width  = models.IntegerField()
    length  = models.IntegerField()
    limit_weight = models.FloatField()
    def __str__(self):
        return self.type

class TypeCargo(models.Model):
    type = models.CharField(max_length=20)
    height = models.IntegerField()
    width  = models.IntegerField()
    length  = models.IntegerField()
    color = models.CharField(max_length=50)
    def __str__(self):
        return self.type

class Container(models.Model):
    type_container = models.ForeignKey(
        "TypeContainer", on_delete=models.CASCADE)
    weight_pack = models.FloatField(default=0.0)
    project_id = models.ForeignKey(
        "Project", on_delete=models.CASCADE)
    
    
class Cargoes(models.Model):
    name = models.CharField(max_length=100)
    type_cargo = models.ForeignKey(
        "TypeCargo", on_delete=models.CASCADE)
    weight = models.FloatField()
    project_id = models.ForeignKey(
        "Project", on_delete=models.CASCADE)
    
class Project(models.Model):
    name = models.CharField(max_length=200)
    cargoes_qty = models.IntegerField()
    cargoes_packed = models.IntegerField()
    container_qty = models.IntegerField()
    container_used = models.IntegerField()
    fitness = models.FloatField()
    weight_check = models.BooleanField(default=False)
    user = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Position(models.Model):
    X = models.IntegerField()
    Y = models.IntegerField()
    Z = models.IntegerField()
    cargoes_id = models.ForeignKey(
        "Cargoes", on_delete=models.CASCADE)
    container_id = models.ForeignKey(
        "Container", on_delete=models.CASCADE)
    
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']