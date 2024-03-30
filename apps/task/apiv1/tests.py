from rest_framework.test import APITestCase
from rest_framework.test import URLPatternsTestCase
from rest_framework.test import APIClient

from rest_framework import status

from django.urls import path
from django.urls import include
from django.urls import reverse


from apps.task import models
from apps.task.apiv1 import serializers


def create_task(title = "Note", description = "Note Description", is_complete = False):
	return models.Task.objects.create(title = title, description = description, is_complete = is_complete)

def serializer_create_task(task):
	return serializers.CreateTaskSerializer(task)

def serializer_detail_task(task):
	return serializers.TasksSerializer(task)

def detail_task(task_id):
	return reverse('task-detail', args = [task_id] )


class TaskAPITest(APITestCase, URLPatternsTestCase):
	urlpatterns = [
		path("todo/api/v1/", include('apps.task.apiv1.urls'))
	]

	def setUp(self):
		self.client = APIClient()

   
	def test_get_tasks(self):
		"""
		ALL TASKS
		"""
		create_task(title = 'Note 1')
		create_task(title = 'Note 2')


		url = reverse('tasks')

		response = self.client.get(url, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(models.Task.objects.count(), 2)


	def test_get_tasks_pagination(self):
		"""
		get task pagination
		"""

		for i in range(11):
			create_task(title = f'Note {i}')

		url = reverse('tasks')

		response = self.client.get(url, format="json")

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		self.assertLessEqual(len(response.data), 5)


	def test_create_task(self):
		"""
		CREATE A TASK
		"""
		
		url = reverse('create-task')

		data = {
			'title': 'Notas App',
			'description': 'Una aplicación de notas',
		}

		response = self.client.post(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(models.Task.objects.get().title, 'Notas App')

	def test_create_ivalid_task(self):
		"""
		create invalid task
		"""
		
		url = reverse('create-task')

		data = {
			'title': 'Notas App',
		}

		response = self.client.post(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


	def test_detail_task(self):
		"""
		DEATIL OF A TASK
		"""
		task = create_task(title = "Note 1")
		serilizer_task = serializer_detail_task(task)

		url = detail_task(task.id)

		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['id'], task.id)
		self.assertEqual(response.data, serilizer_task.data)


	def test_detail_task_not_exist(self):
		"""
		detail task that does not exist
		"""
		url = detail_task(1)

		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



	def test_update_task(self):
		"""
		UPDATE A TASK
		"""
		task = create_task(title = "Nota 1")
		serilizer_task = serializer_create_task(task)

		url = detail_task(task.id)

		data = {
			'title': 'App Notes',
			'description': 'App for write a somes notes',
			'is_complete': True
		}

		response = self.client.put(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertNotEqual(response.data, serilizer_task.data)

	def test_update_task_not_exist(self):
		"""
		update task that does not exist
		"""

		url = detail_task(1)

		data = {
			'title': 'App Notes',
			'description': 'App for write a somes notes',
		}

		response = self.client.put(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


	def test_update_task_duplicate_title(self):
		"""
		update a task with an existing title
		"""
		task = create_task(title = "Note 1")

		url = detail_task(task.id)

		data = {
			'title': 'Note 1',
			'description': 'App to write some notes',
			'is_complete': True
		}

		response = self.client.put(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_update_ivnvalid_task(self):
		"""
		update invalidly
		"""
		task = create_task(title = "Note 1")

		url = detail_task(task.id)

		data = {
			'title': '',
			'description': '',
			'is_complete': False
		}

		response = self.client.put(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


	def test_patch_task(self):
		"""
		UPDATE PARTIAL TASK
		"""
		task = create_task(title = "Nota 1")
		serilizer_task = serializer_create_task(task)

		url = detail_task(task.id)

		data = {
			'is_complete': True
		}

		response = self.client.patch(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertNotEqual(response.data, serilizer_task.data)
		self.assertTrue(response.data['is_complete'])

	def test_patch_task_duplicate_title(self):
		"""
		partial update of a task with an existing title
		"""
		task = create_task(title = "Note 1")

		url = detail_task(task.id)

		data = {
			'title': 'Note 1',
		}

		response = self.client.patch(url, data, format='json')
		
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_patch_task_not_exist(self):
		"""
		partial update of a task that does not exist
		"""

		url = detail_task(1)

		data = {
			'title': 'App Notes',
		}

		response = self.client.patch(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


	def test_patch_ivnvalid_task(self):
		"""
		invalid partial update
		"""
		task = create_task(title = "Note 1")

		url = detail_task(task.id)

		data = {
			'title': ''
		}

		response = self.client.patch(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


	def test_delete_task(self):
		"""
		DELETE A TASK
		"""
		task = create_task(title = "Nota 1")

		url = detail_task(task.id)

		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


	def test_delete_task_not_exist(self):
		"""
		delete task that does not exist
		"""
		url = detail_task(1)

		response = self.client.delete(url)
		
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)




		











		
