from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
	path("task/create/", views.CreateTaskAV.as_view(), name = "create-task"),
	path("tasks/", views.AllTaskAV.as_view(), name = "tasks"),
	path("task/<int:pk>/", views.TaskDetailAV.as_view(), name = "task-detail"),
]
