from django.urls import path
from . import views

# name space for better work with URLS
app_name = 'exams'

urlpatterns = [
    path('lesson/<int:lesson_id>', views.exam_overview, name='welcome'),
    path('lesson/exam/<int:lesson_id>', views.exam_view, name='exam'),
    path('', views.exam_view, name='exam'),
    path('all/', views.exam_all, name='all'),
]
