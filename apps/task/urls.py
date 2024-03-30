from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
	path('task/create/', views.CreateTaskFormView.as_view(), name = "create-task"),
	path('task/list/', views.TasksListView.as_view(), name = "list-task"),
	path('task/<int:pk>/detail/', views.DetailTaskDetailView.as_view(), name = "detail-task"),
	path('task/<int:pk>/info/update/', views.UpdateInfoTaskView.as_view(), name = "update-task"),
	path('task/<int:pk>/status/update/', views.CompleteTaskView.as_view(), name = "update-status-task"),
	path('task/<int:pk>/delete/', views.DeleteTaskView.as_view(), name = "delete-task"),
]