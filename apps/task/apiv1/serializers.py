
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.task import models

USER_ID = 1

class TasksSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Task
		fields = "__all__"


class TasksListSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Task
		fields = ['id','user_id', 'title']


class CreateTaskSerializer(serializers.ModelSerializer):
	
	def validate_title(self, value):
		
		if models.Task.objects.filter(user_id = USER_ID, title = value).exists():
			raise serializers.ValidationError('A task with this title already exists')
		
		if len(value) < 4:
			raise serializers.ValidationError('The title is very short')
		return value

	class Meta:
		model = models.Task
		fields = ['title', 'description', 'is_complete']
		extra_kwargs = {
			'is_complete': {
				'required': False
			}
		}




class TasksUpdateSerializer(serializers.ModelSerializer):
	def validate_title(self, value):
		
		if models.Task.objects.filter(user_id = USER_ID, title = value).exists():
			raise serializers.ValidationError('A task with this title already exists')
		
		if len(value) < 4:
			raise serializers.ValidationError('The title is very short')
		return value

	class Meta:
		model = models.Task
		fields = ['title', 'description', 'is_complete']



