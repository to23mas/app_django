from django.urls import path
from . import views

# name space for better work with URLS
app_name = 'lessons'

urlpatterns = [
    path('lesson/<int:lesson_id>/<str:chapter_link>', views.switch_view, name='switch'),
    path('lesson/UVOD/<str:chapter_link>', views.lessonOne_view, name='lessonOne'),
    path('lesson/HELLO/<str:chapter_link>', views.lessonTwo_view, name='lessonTwo'),
    path('lesson/<str:not_>', views.not_view, name='not'),
]

