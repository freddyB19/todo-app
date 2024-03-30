from django.test import TestCase
from django.urls import reverse

from apps.task import models 

def create_task(title = "Note", description = "Note Description", is_complete = False):
	return models.Task.objects.create(title = title, description = description, is_complete = is_complete)

class TaskModelTest(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		create_task()
	
	def test_title_label(self):
		"""
		"""
		task = models.Task.objects.get(pk = 1)

		title_label = task._meta.get_field('title').verbose_name

		self.assertEqual(title_label, 'Title')

	def test_title_max_length(self):
		task = models.Task.objects.get(id = 1)

		max_length = task._meta.get_field('title').max_length

		self.assertEqual(max_length, 30)

	def test_description_label(self):
		"""
		"""
		task = models.Task.objects.get(pk = 1)

		description_label = task._meta.get_field('description').verbose_name

		self.assertEqual(description_label, 'Description')

	def test_is_complete_label(self):
		"""
		"""
		task = models.Task.objects.get(pk = 1)
		
		is_complete_label = task._meta.get_field('is_complete').verbose_name

		self.assertEqual(is_complete_label, 'Status')

	def test_is_complete_default(self):

		task = models.Task.objects.get(pk = 1)

		is_complete_default = task._meta.get_field('is_complete').default

		self.assertEqual(is_complete_default, False)

	def test_created_auto_now_add(self):
		
		task = models.Task.objects.get(pk = 1)

		created_auto_now_add = task._meta.get_field('created').auto_now_add

		self.assertEqual(created_auto_now_add, True)

	def test_updated_auto_now(self):
		task = models.Task.objects.get(pk = 1)

		created_auto_now = task._meta.get_field('updated').auto_now

		self.assertEqual(created_auto_now, True)

	def test_object_name_is_title_user_id(self):
		"""
		"""

		task = models.Task.objects.get(pk = 1)

		object_name = f"{task.title} - user : {task.user_id}"

		self.assertEqual(object_name, str(task))

	def test_get_absolute_url(self):
		"""
		"""
		task = models.Task.objects.get(pk = 1)

		self.assertEqual(task.get_absolute_url(), f'/todo/task/{task.id}/detail/')









