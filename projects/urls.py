from django.urls import path
from . import views

# name space for better work with URLS
app_name = 'projects'

urlpatterns = [
    path('hello_world/', views.hello_view, name='hello_world'),
    path('todo/', views.todo_view, name='todo'),
    path('todo_two/', views.todo_two_view, name='todo_two'),
    path('todo_two/<int:todo_id>/', views.delete_todo, name='delete'),
    path('all/', views.all_view, name='all'),
    path('register_one/', views.accounts_register_view, name='register_one'),
    path('login_one/', views.accounts_login_one, name='login_one'),
    path('account_cross/', views.cross_view, name='cross'),
    path('done/', views.done_view, name='done'),

]

