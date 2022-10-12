from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'coffee'
urlpatterns = [
<<<<<<< HEAD
=======
	path('index/', views.index, name='index'),
>>>>>>> f7b981b94152cba8534f636711ea8641d2941261
	path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('userView/', views.userView, name='userView'),
    path('managerView/', views.managerView, name='managerView'),
<<<<<<< HEAD
    path('manageEmployees/', views.manageEmployees, name='manageEmployees'),
=======
>>>>>>> f7b981b94152cba8534f636711ea8641d2941261
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/update/<int:pk>/', views.update_inventory, name="update-inventory")
]
