from django.test import  SimpleTestCase

from apps.task import forms 


class TaskFormTest(SimpleTestCase):

	@classmethod
	def setUpTestData(cls):
		self.form = forms.CreateTaskForm()



	def test_title_label(self):
		form = forms.CreateTaskForm()

		self.assertEqual(form.fields['title'].label, 'Title')
		
		self.assertTrue(
			form.fields['title'].label == None or form.fields['title'].label == 'Title'
		)


	def test_title_max_length(self):
		form = forms.CreateTaskForm()

		self.assertEqual(form.fields['title'].max_length, 30)


	def test_title_min_length(self):
		form = forms.CreateTaskForm()

		self.assertEqual(form.fields['title'].min_length, 4)


	def test_description_label(self):
		form = forms.CreateTaskForm()

		self.assertEqual(form.fields['description'].label, 'Description')
		
		self.assertTrue(
			form.fields['description'].label == None or form.fields['description'].label == 'Description'
		)

	def test_description_max_length(self):
		form = forms.CreateTaskForm()

		self.assertEqual(form.fields['description'].max_length, 300)

	def test_status_label(self):
		form = forms.SearchTaskStatusForm()

		self.assertEqual(form.fields['status'].label, 'Status')

	def test_status_choices(self):
		form = forms.SearchTaskStatusForm()

		CHOICES_STATUS = [
			(True, 'Completed Tasks'),
			(False, 'Not Completed Tasks'),
			('all', 'View All Tasks'),
		]

		self.assertEqual(form.fields['status'].choices, CHOICES_STATUS)







