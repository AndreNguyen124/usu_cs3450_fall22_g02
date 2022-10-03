from django.urls import path
from . import views

# URLConf module (url configuration)
urlpatterns = [
    #    the route (url)   a view function (but don't call it, just reference it)
    path('hello/', views.say_hello, name='hello'),
    
    path('register/', views.registerPage, name = 'register'),
    path('login/', views.loginPage, name = 'login')
]