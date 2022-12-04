from django.urls import path

from . import views

app_name = 'coffee'
urlpatterns = [
	path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('userView/', views.userView, name='userView'),
    path('userView/update-balance/', views.update_account_balance, name='update-balance'),
    path('userView/update-hours/', views.update_hours, name='update-hours'),
    path('employeeView/', views.employeeView, name='employeeView'),
    path('managerView/', views.managerView, name='managerView'),
    path('deliver-drinks/', views.deliverDrinks, name='deliverDrinks'),
    path('pay-employees/', views.payEmployees, name='pay-employees'),
    path('manageEmployees/', views.manageEmployees, name='manageEmployees'),
    path('manageEmployees/paidOrders/<int:pk>/', views.viewPaidOrders, name='paidOrders'),
    path('createEmployee/', views.createEmployee, name='createEmployee'),

    path('inventory/', views.inventory, name='inventory'),
    path('inventory/update/<int:pk>/', views.update_inventory, name="update-inventory"),

    path('drink', views.drinkProduct, name="drink"),
    path('customizeDrink/<int:pk>/', views.customizeDrink, name='customizeDrink'),

    path('userViewEmployee/', views.userViewEmployee, name='userViewEmployee'),
    path('customizeDrinkEmployee/<int:pk>/', views.customizeDrinkEmployee, name='customizeDrinkEmployee'),

    path('drink/update-markup/', views.update_markup, name='update-markup'),
    path('drink/drink_delete/<int:pk>/', views.product_delete, name="drink_delete"),
    path('drink/drink_add/<int:pk>/', views.addDrinkProduct, name="drink_add"),
    path('drink/drink_update/<int:pk>/', views.product_update, name="drink_update"),

    path('edit-menu/', views.menuItem, name="edit-menu"),
    path('edit-menu/menu_add/', views.addMenuItem, name="menu_add"),
    path('edit-menu/menu_delete/<int:pk>/', views.deleteMenuItem, name="menu_delete"),
    path('edit-menu/menu_update/<int:pk>/', views.menu_update, name="menu_update"),

    path('shopping_cart/', views.shoppingCartView, name="shopping_cart"),

    path('notAuth.html/', views.notAuth, name='notAuth'),

]
