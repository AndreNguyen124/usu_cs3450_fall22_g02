from django.urls import path

from . import views

app_name='dans_cool_beans'
urlpatterns = [
    path('inventory', views.manage_inventory, name='manage_inventory'),
]
