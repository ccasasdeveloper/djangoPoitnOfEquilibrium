from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

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


class VariableEconomic(models.Model):
    nameVariable = models.CharField(max_length=64)
    value = models.FloatField()

    def __str__(self):
        return f"{self.nameVariable} - its value is {self.value}"




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


    def __str__(self):
        return f"{self.name}"


class Projection(models.Model):
    name = models.CharField(max_length=64)
    type = models.ForeignKey(ProjectionType, on_delete=models.CASCADE, related_name="projectionType")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    count = models.FloatField()

    def __str__(self):
        return f"{self.nombre}"
