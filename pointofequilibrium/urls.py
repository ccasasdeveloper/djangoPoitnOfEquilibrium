from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("admin", admin.site.urls, name="admin"),
    path(r'^register/$', views.register, name='register'),
    path("product_choose",views.product_choose, name='product_choose'),
    
    
    ]
