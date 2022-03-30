from django.urls import path
from . import views

# name space for better work with URLS
app_name = 'projects'

urlpatterns = [
    path('hello_world/', views.hello_view, name='hello_world'),

]

