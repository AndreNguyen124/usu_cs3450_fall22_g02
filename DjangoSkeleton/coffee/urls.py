from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'coffee'
urlpatterns = [
	path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('userView/', views.userView, name='userView'),
    path('customizeDrink/', views.customizeDrink, name='customizeDrink'),
    path('employeeView/', views.employeeView, name='employeeView'),
    path('managerView/', views.managerView, name='managerView'),
    path('manageEmployees/', views.manageEmployees, name='manageEmployees'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/update/<int:pk>/', views.update_inventory, name="update-inventory"),
    path('drink', views.drinkProduct, name="drink"),
    path('drink/update-markup/', views.update_markup, name='update-markup'),
    path('drink/drink_delete/<int:pk>/', views.product_delete, name="drink_delete"),
    path('drink/drink_add/<int:pk>/', views.addDrinkProduct, name="drink_add"),
    path('drink/drink_update/<int:pk>/', views.product_update, name="drink_update"),

]
