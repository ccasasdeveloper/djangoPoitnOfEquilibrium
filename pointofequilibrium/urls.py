from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("admin", admin.site.urls, name="admin"),
    path(r'^register/$', views.register, name='register'),
    path("<int:product_id>/<int:user_id>/product_choose",views.product_choose, name='product_choose'),
    path("<int:product_id>/<int:user_id>/form_values_bank", views.form_values_bank, name='form_values_bank'),
    path("<int:user_id>/historial", views.historial, name='historial'),
    path("checkNewTemplate", views.checkNewTemplate, name="checkNewTemplate"),
    ]
