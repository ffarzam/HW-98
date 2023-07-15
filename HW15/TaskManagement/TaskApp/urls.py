from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks/<int:pk>/', views.task_details, name="task_details"),
    path('search/', views.search, name='search'),
    path('search_result/', views.search_result, name='search_result'),
]
