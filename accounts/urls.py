from django.urls import path
from . import views

# name space for better work with URLS
app_name = 'accounts'

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout')
]
