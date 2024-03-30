import datetime
from django.db import models
from django.urls import reverse


# Create your models here.

class Task(models.Model):
	user_id = models.SmallIntegerField(default = 1)
	title = models.CharField('Title', max_length=30)
	description = models.TextField('Description')
	is_complete = models.BooleanField("Status", default = False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ['user_id', 'title']


	def get_absolute_url(self):
		return reverse('tasks:detail-task', kwargs = {'pk': self.pk})
	
	def __str__(self):
		return f"{self.title} - user : {self.user_id}"



