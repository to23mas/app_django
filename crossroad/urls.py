from django.urls import path
from . import views

# name space for better work with URLS
app_name = 'crossroad'

urlpatterns = [
    path('', views.welcome, name='welcome'),

]
