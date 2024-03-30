#from django.shortcuts import render

from django.views import View
from django.views import generic
from django.views.generic import edit

from django.urls import reverse
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from . import models
from . import forms


USER_ID = 1

# Create your views here.
class CreateTaskFormView(edit.FormView):
	form_class = forms.CreateTaskForm
	model = models.Task
	template_name = "task/create_task.html"
	success_url = reverse_lazy('tasks:create-task')
	
	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({
			'user_id': USER_ID
		})
		return kwargs

	def form_valid(self, form):
		if form.is_valid():
			form.save()
			messages.add_message(self.request, messages.INFO, 'A task has been created')
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    tasks = models.Task.objects.filter(user_id = USER_ID).order_by('-id')
	    context['tasks_user'] = tasks[:5]
	    context['tasks_count'] = tasks.count()
	    return context

class TasksListView(generic.ListView):
	model = models.Task
	paginate_by = 3
	context_object_name = 'tasks'
	template_name = 'task/list_tasks.html'

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    data = self.request.GET if self.request.GET.get('status', '') else {'status': 'all'}
	    context['form_status'] = forms.SearchTaskStatusForm(initial = data)
	    return context
	
	def get_queryset(self):
		status = self.request.GET.get('status', 'all')
		
		if status ==  'all':
			return models.Task.objects.filter(user_id = USER_ID).order_by('-id')
		return models.Task.objects.filter(user_id = USER_ID, is_complete = status).order_by('-id')
		

class DetailTaskDetailView(generic.DetailView):
	model = models.Task
	context_object_name = 'task'
	template_name = 'task/detail_task.html'

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['user_id'] = USER_ID
	    return context

class UpdateInfoTaskView(edit.FormView):
	model = models.Task
	form_class = forms.UpdateTaskFrom
	template_name = 'task/update_task.html'
	success_url = reverse_lazy("tasks:list-task")

	def get_form_kwargs(self):
	    """Return the keyword arguments for instantiating the form."""
	    kwargs = {
	        "initial": self.get_initial(),
	        "prefix": self.get_prefix(),
	    }
	    if self.request.method in ("POST", "PUT"):
	        kwargs.update(
	            {
	                "data": self.request.POST,
	                "files": self.request.FILES,
	            }
	        )
	   
	    elif self.request.method == "GET":
	    	task = models.Task.objects.get(pk = self.kwargs.get("pk"))
	    	print(task.__dict__)
	    	kwargs.update({
	    		"data": task.__dict__
	    	})

	    return kwargs

	
	def form_valid(self, form):
		if form.is_valid():
			try:
				task = get_object_or_404(models.Task, pk = self.kwargs['pk'], user_id = USER_ID)
				task.title = form.cleaned_data['title']
				task.description = form.cleaned_data['description']
				task.is_complete = form.cleaned_data['is_complete']

				
				messages.add_message(self.request, messages.SUCCESS, 'The task has been updated')

				task.save()
			except models.Task.DoesNotExist as e:
				messages.add_message(self.request, messages.ERROR, 'This user does not have a task with that id')
		
		return super(UpdateInfoTaskView, self).form_valid(form)


class CompleteTaskView(View):
	def post(self, request, pk, *args,**kwargs):
		try:
			task = get_object_or_404(models.Task, pk = pk, user_id = USER_ID)
			task.is_complete = True
			task.save()
			messages.add_message(request, messages.SUCCESS, 'A task has been completed')

		except models.Task.DoesNotExist as e:
			messages.add_message(request, messages.ERROR, 'This user does not have a task with that id')
			
		return HttpResponseRedirect(reverse('tasks:list-task'))


class DeleteTaskView(View):

	def post(self, request, pk, *args, **kwargs):
		try:
			task = get_object_or_404(models.Task, pk = pk, user_id = USER_ID)
			task.delete()
			messages.add_message(request, messages.INFO, 'Task deleted with success')
		
		except models.Task.DoesNotExist as e:
			messages.add_message(request, messages.ERROR, 'This user does not have a task with that id')

		return HttpResponseRedirect(reverse('tasks:list-task'))





