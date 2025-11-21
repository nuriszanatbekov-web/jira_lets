from django.urls import path
from . import views

urlpatterns = [
    path('', views.kanban_board, name='kanban_board'),
    path('update/<int:task_id>/', views.update_status, name='update_status'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
]
