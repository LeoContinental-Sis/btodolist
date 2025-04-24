from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.todo_list_create),
    path('todos/<int:pk>/', views.todo_detail_update_delete),
]