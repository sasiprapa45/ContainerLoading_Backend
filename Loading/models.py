from django.db import models

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

    def __str__(self):
        return self.type

class Container(models.Model):
    type_container = models.ForeignKey(
        "TypeContainer", on_delete=models.CASCADE)
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
    
