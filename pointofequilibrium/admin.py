from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.admin import ModelAdmin, actions

# Register your models here.
from .models import  ProductType, ProjectionType,  Product, VariableEconomic, Projection, UserProfile, Duration, Bank

class MyUserAndmin(admin.ModelAdmin):
    list_display = ('username','date_joined','is_superuser')
    list_filter = ('date_joined',)



admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, MyUserAndmin)
admin.site.site_header = 'Punto de equlibrio'
admin.site.register(Bank)
admin.site.register(VariableEconomic)
admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(ProjectionType)
admin.site.register(Projection)
admin.site.register(Duration)
