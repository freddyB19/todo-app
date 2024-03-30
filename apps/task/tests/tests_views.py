import random

from django.urls import reverse

from django.test import TestCase

from apps.task import models
from apps.task import forms 

# Create your tests here.

def create_task(title = "Note", description = "Note Description", is_complete = False):
	return models.Task.objects.create(title = title, description = description, is_complete = is_complete)

def get_url_task(url_name, task_id = 1):
	return reverse(url_name, args = [task_id])

class TaskViewTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		for i in range(15):
			if i >= 6:
				create_task(title = f'Note {i}', is_complete = False)
			else:
				create_task(title = f'Note {i}', is_complete = True)

	@classmethod
	def tearDownClass(cls):
		models.Task.objects.all().delete()


	def test_view_list_task_url_exists_at_desired_location(self):
		response = self.client.get('/todo/task/list/')

		self.assertEqual(response.status_code, 200)

	def test_view_list_task_url_by_name(self):
		response = self.client.get(reverse('tasks:list-task'))

	def test_view_create_task_url_exists_at_desired_location(self):
		response = self.client.get('/todo/task/create/')

	def test_view_create_task_url_by_name(self):
		response = self.client.get(reverse('tasks:create-task'))

		self.assertEqual(response.status_code, 200)

	def test_view_update_task_url_by_name(self):
		response = self.client.get(reverse('tasks:update-task', kwargs = {'pk': 1}))

		self.assertEqual(response.status_code, 200)

	def test_view_update_status_task_url_by_name(self):
		response = self.client.post(reverse('tasks:update-status-task', kwargs = {'pk': 1}))

		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse("tasks:list-task"))

	
	def test_view_detail_task_url_by_name(self):
		response = self.client.get(reverse('tasks:detail-task', kwargs = {'pk': 1}))

		self.assertEqual(response.status_code, 200)

	def test_view_delete_task_url_by_name(self):
		response = self.client.post(reverse('tasks:delete-task', kwargs = {'pk': 1}))
		
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse("tasks:list-task"))


	def test_create_task_correct_tamplate(self):
		response = self.client.get(reverse('tasks:create-task'))

		self.assertTemplateUsed(response, 'task/create_task.html')

	def test_list_tasks_correct_tamplate(self):
		response = self.client.get(reverse('tasks:list-task'))
		
		self.assertTemplateUsed(response, 'task/list_task.html')

	def test_list_tasks_correct_tamplate(self):
		response = self.client.get(reverse('tasks:detail-task', kwargs = {'pk': 1}))
		
		self.assertTemplateUsed(response, 'task/detail_task.html')

	def test_list_tasks_pagination(self):
		response = self.client.get(reverse('tasks:list-task') + '?page=2')
		
		self.assertEqual(response.status_code, 200)
		self.assertTrue('is_paginated' in response.context)
		self.assertTrue(len(response.context['tasks']) == 3)

	def test_list_task_filter_by_field_is_complete(self):
		response_complete_true = self.client.get(reverse('tasks:list-task') + '?is_complete=true')
		response_complete_false = self.client.get(reverse('tasks:list-task') + '?is_complete=false')

		self.assertEqual(response_complete_true.status_code, 200)
		self.assertEqual(response_complete_false.status_code, 200)

		self.assertEqual(len(response_complete_true.context['tasks']), 3)
		self.assertEqual(len(response_complete_false.context['tasks']), 3)


	def test_create_some_task(self):
		data_valid = {'title': 'Some Note', 'description': 'Note Description'}
		data_invalid = {'title': 'Some Note'}


		form_valid = forms.CreateTaskForm(data = data_valid)
		form_invalid = forms.CreateTaskForm(data = data_invalid)


		self.assertTrue(form_valid.is_valid())
		self.assertFalse(form_invalid.is_valid())


	def test_update_valid_task(self):
		task = models.Task.objects.get(id = random.randint(1, 14))

		data = {'title': 'Some Note', 'description': 'Note Description'}

		response = self.client.post(reverse('tasks:update-task', kwargs = {'pk': task.id}), data)
		

		task_updated = models.Task.objects.get(id = task.id)

		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse("tasks:list-task"))
		self.assertNotEqual(task.title, task_updated.title)

	def test_update_complete_task(self):
		task = models.Task.objects.get(id = random.randint(7, 14))

		data = {'is_complete': True}

		response = self.client.post(reverse('tasks:update-status-task', kwargs = {'pk': task.id}), data)

		task_updated = models.Task.objects.get(id = task.id)

		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse("tasks:list-task"))
		self.assertNotEqual(task.is_complete, task_updated.is_complete)

	def test_update_invalid_task(self):

		data_valid = {'title': 'Some Note', 'description': 'Note Description'}

		response = self.client.post(reverse('tasks:update-task', kwargs = {'pk': 300}), data_valid)

		self.assertEqual(response.status_code, 404)

	def test_detail_valid_task(self):
		task = models.Task.objects.get(id = random.randint(1, 14))
		
		response = self.client.get(reverse('tasks:detail-task', kwargs = {'pk': task.id}))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['task'].title, task.title)

	def test_detail_invalid_task(self):

		response = self.client.get(reverse('tasks:detail-task', kwargs = {'pk': 300}))

		self.assertEqual(response.status_code, 404)

	def test_delete_valid_task(self):
		task = models.Task.objects.get(id = random.randint(1, 14))
		
		response = self.client.post(reverse('tasks:delete-task', kwargs = {'pk': task.id}))

		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse("tasks:list-task"))

	def test_delete_invalid_task(self):

		response = self.client.post(reverse('tasks:delete-task', kwargs = {'pk': 300}))

		self.assertEqual(response.status_code, 404)

	def test_delete_task_no_exist(self):
		task = models.Task.objects.get(id = random.randint(1, 14))

		response = self.client.post(reverse('tasks:delete-task', kwargs = {'pk': task.id}))

		self.assertEqual(response.status_code, 302)

		response = self.client.post(reverse('tasks:delete-task', kwargs = {'pk': task.id}))
		self.assertEqual(response.status_code, 404)











































	
	def test_delete_some_task(self):
		pass


		#assertTemplateUsed
		#assertRedirects

		









