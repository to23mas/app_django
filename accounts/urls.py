from django.urls import path
from . import views

# name space for better work with URLS
app_name = 'accounts'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]
