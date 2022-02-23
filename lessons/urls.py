from django.urls import path
from . import views

# name space for better work with URLS
app_name = 'lessons'

urlpatterns = [
    path('<int:lesson_id>/welcome/', views.welcome_view, name='welcome'),
    path('<int:lesson_id>/<str:chapter>', views.chapter_view, name='chapter')

]
