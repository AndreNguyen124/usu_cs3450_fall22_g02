from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'coffee'
urlpatterns = [
	path('login', views.login, name='login'),
    path('userView', views.userView, name='userView'),
    path('managerView', views.managerView, name='managerView'),
    path('manageEmployees', views.manageEmployees, name='manageEmployees'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/update/<int:pk>/', views.update_inventory, name="update-inventory")
]
