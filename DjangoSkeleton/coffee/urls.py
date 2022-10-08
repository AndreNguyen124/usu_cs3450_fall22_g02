from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'coffee'
urlpatterns = [
	path('index', views.index, name='index'),
	path('login', views.login, name='login'),
    path('inventory', views.manage_inventory, name='manage_inventory'),
]
