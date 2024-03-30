from django import forms

from . import models

class TaskbaseForm(forms.Form):
	title = forms.CharField(
		label = 'Title', 
		max_length = 30, 
		min_length = 4,
		widget=forms.TextInput(
		 	attrs = {
		 		'class': 'form-control'
		 	}
		 )
	)
	description = forms.CharField(
		label = 'Description',
		 max_length = 300, 
		 widget=forms.Textarea(
		 	attrs = {
		 		'class': 'form-control',
		 		'rows': 3
		 	}
		 )
	)


class CreateTaskForm(TaskbaseForm):

	def __init__(self, user_id = None,*args, **kwargs):
	    super().__init__(*args, **kwargs)
	    self.user_id = user_id

	def clean_title(self):
		title = self.cleaned_data['title']

		if models.Task.objects.filter(user_id = self.user_id, title = title).exists():
			self.add_error('title', 'A task with that title already exists.')
		return title
	
	def save(self):
		return models.Task.objects.create(
			title = self.cleaned_data['title'],
			description = self.cleaned_data['description'],
		)

class UpdateTaskFrom(forms.Form):
	title = forms.CharField(
		label = 'Title', 
		required=True,
		widget=forms.TextInput(
		 	attrs = {
		 		'class': 'form-control'
		 	}
		 )
	)
	description = forms.CharField(
		label = 'Description',
		required=True,
		widget=forms.Textarea(
		 	attrs = {
		 		'class': 'form-control',
		 		'rows': 3
		 	}
		 )
	)

	is_complete = forms.BooleanField(
		label = 'Status',
		required=False, 
	)

	


class SearchTaskStatusForm(forms.Form):
	COMPLETE = True
	NO_COMPLETE = False
	TODAS = 'all'

	CHOICES_STATUS = [
		(COMPLETE, 'Completed Tasks'),
		(NO_COMPLETE, 'Not Completed Tasks'),
		(TODAS, 'View All Tasks'),
	]
	status = forms.ChoiceField(
		label = "Status",
		choices=CHOICES_STATUS, 
		widget=forms.Select(
			attrs = {
				'class': 'form-select form-control'
			}
		)
	)
