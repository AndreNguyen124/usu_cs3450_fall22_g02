from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'coffee'
urlpatterns = [
	path('index', views.index, name='index'),
	path('login', views.login, name='login'),
    path('userView', views.userView, name='userView'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/update/<int:pk>/', views.update_inventory, name="update-inventory")
]
