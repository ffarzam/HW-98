from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks/<int:pk>/', views.task_details, name="task_details"),
    path('search/', views.search, name='search'),
    path('search_result/', views.search_result, name='search_result'),
    path('category/', views.category, name='category'),
    path('category_task/<int:pk>/', views.category_task, name='category_task'),
    path('about_us', views.about_us, name='about_us'),
    path('download_file/<filename>', views.download_file, name='download_file'),

]
# path('view_file/<filename>', views.view_file, name='view_file'),
