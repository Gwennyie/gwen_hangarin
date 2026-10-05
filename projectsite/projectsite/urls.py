"""
URL configuration for projectsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tasks import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")), # allauth routes
    path('', views.HomePageView.as_view(), name='home'),

    path('tasks/', views.TaskList.as_view(), name='task-list'),
    path('tasks/add', views.TaskCreateView.as_view(), name='task-add'),
    path('tasks/<pk>', views.TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<pk>/delete', views.TaskDeleteView.as_view(), name='task-delete'),

    path('notes/', views.NoteList.as_view(), name='note-list'),
    path('notes/add', views.NoteCreateView.as_view(), name='note-add'),
    path('notes/<pk>', views.NoteUpdateView.as_view(), name='note-update'),
    path('notes/<pk>/delete', views.NoteDeleteView.as_view(), name='note-delete'),

    path('subtasks/', views.SubTaskList.as_view(), name='subtask-list'),
    path('subtasks/add', views.SubTaskCreateView.as_view(), name='subtask-add'),
    path('subtasks/<pk>', views.SubTaskUpdateView.as_view(), name='subtask-update'),
    path('subtasks/<pk>/delete', views.SubTaskDeleteView.as_view(), name='subtask-delete'),

    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/add', views.CategoryCreateView.as_view(), name='category-add'),
    path('categories/<pk>', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<pk>/delete', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('priorities/', views.PriorityList.as_view(), name='priority-list'),
    path('priorities/add', views.PriorityCreateView.as_view(), name='priority-add'),
    path('priorities/<pk>', views.PriorityUpdateView.as_view(), name='priority-update'),
    path('priorities/<pk>/delete', views.PriorityDeleteView.as_view(), name='priority-delete'),
]