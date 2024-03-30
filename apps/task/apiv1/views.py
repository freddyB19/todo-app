from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView

from rest_framework import response
from rest_framework import filters as rest_filters

from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from apps.task import models

from . import pagination
from . import serializers
from . import throlling

USER_ID = 1


class CreateTaskAV(generics.CreateAPIView):
	serializer_class = serializers.CreateTaskSerializer
	throttle_classes = [throlling.CreateTaskThrottle]



class AllTaskAV(generics.ListAPIView):
	serializer_class = serializers.TasksListSerializer
	pagination_class = pagination.TasksListPaginationLO
	filter_backends = (filters.DjangoFilterBackend, rest_filters.SearchFilter)
	filterset_fields = ("is_complete",)
	throttle_classes = [throlling.ListTaskThrottle]


	def get_queryset(self):
		return models.Task.objects.filter(user_id = USER_ID).order_by("-id")


class TaskDetailAV(APIView):
	def get(self, request, pk):
		try:
			task = models.Task.objects.get(pk = pk, user_id = USER_ID)
		except models.Task.DoesNotExist:
			return response.Response(data = {'error': {'message': 'There is no task with this id'}}, status = status.HTTP_404_NOT_FOUND)

		de_serializer_task = serializers.TasksSerializer(task)
		
		return response.Response(data = de_serializer_task.data, status = status.HTTP_200_OK)


	def put(self, request, pk):
		try:
			task = models.Task.objects.get(pk = pk, user_id = USER_ID)
		except models.Task.DoesNotExist as e:
			return response.Response(data = {'error': {'message': 'There is no task with this id'}}, status = status.HTTP_404_NOT_FOUND)

		de_serializer_task = serializers.TasksUpdateSerializer(task, request.data)
		
		if de_serializer_task.is_valid():
			de_serializer_task.save()
			
			return response.Response(data = de_serializer_task.data, status = status.HTTP_200_OK)

		return response.Response(data = de_serializer_task.errors, status = status.HTTP_404_NOT_FOUND)

	def patch(self, request, pk):
		try:
			task = models.Task.objects.get(pk = pk, user_id = USER_ID)
		except models.Task.DoesNotExist as e:
			return response.Response(data = {'error': {'message': 'There is no task with this id'}}, status = status.HTTP_404_NOT_FOUND)

		de_serializer_task = serializers.TasksUpdateSerializer(task, request.data, partial = True)
		
		if de_serializer_task.is_valid():
			de_serializer_task.save()
			
			return response.Response(data = de_serializer_task.data, status = status.HTTP_200_OK)

		return response.Response(data = de_serializer_task.errors, status = status.HTTP_404_NOT_FOUND)

	def delete(self, request, pk):
		try:
			task = models.Task.objects.get(pk = pk, user_id = USER_ID)
			task.delete()
		except models.Task.DoesNotExist as e:
			return response.Response(data = {'error': {'message': 'There is no task with this id'}}, status = status.HTTP_404_NOT_FOUND)
		return response.Response(data = {'message': 'Task deleted with success'}, status = status.HTTP_204_NO_CONTENT)
