from django.urls import path
from . import views

# name space for better work with URLS
app_name = 'crossroad'

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('overView/', views.courses_overview_view, name='overview'),
    path('about/', views.about_view, name='about'),

]
