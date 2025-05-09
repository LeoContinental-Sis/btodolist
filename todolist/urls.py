from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.todo_list_create, name='task-list'),
]
