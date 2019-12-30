from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django import forms
    

# Create your models here.



class UserProfile(models.Model):
    date_joined = models.DateTimeField('date joined')
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
            post_save.connect(create_user_profile, sender=User)






class ProductType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    name = models.CharField(max_length=64)
    productType = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="productType")

    def __str__(self):
        return f"{self.name} - {self.productType}"

class ProjectionType(models.Model):
    name = models.CharField(max_length=64)
    productType = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="productTypeOnProjections")

    def __str__(self):
        return f"{self.name}"

class Duration(models.Model):


    time_of_duration = models.CharField(max_length=64)
    limit_lower = models.IntegerField(name="Limite_inferior")
    limit_higher = models.IntegerField(name="limite_superior")

    def __str__(self):
        return f"{self.time_of_duration}"





class Bank(models.Model):

    name = models.CharField(name="Nombre", max_length=64)
    def __str__(self):
        return f"{self.Nombre}"

class VariableEconomic(models.Model):

    nameVariable = models.CharField(max_length=64)
    value = models.FloatField()
    duration = models.ForeignKey(Duration, on_delete=models.CASCADE, related_name="duracion")
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="banco")

    def __str__(self):
        return f"{self.nameVariable} - its value is {self.value}. {self.bank.Nombre}"


        
class Projection(models.Model):
    
    type_of_projection = models.ForeignKey(ProjectionType, on_delete=models.CASCADE, related_name="projectionType")
    amount = models.FloatField()
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    variableEconomic = models.ForeignKey(VariableEconomic, on_delete=models.CASCADE, related_name="variableEconomic")

    def __str__(self):
        return f"Tu hiciste un proyecció el {self.date_modified} basada en un {self.type_of_projection.productType.name}"



