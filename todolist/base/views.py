from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from django.contrib.auth.views import LoginView
from .models import *


# Create your views here.
class TaskList(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count

        search_input= self.request.GET.get('search') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__icontains=search_input)

        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task 
    template_name = 'task_detail.html'
    context_object_name = 'tasks'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    template_name = 'task_create.html'
    fields = ['title','description','complete']
    success_url=reverse_lazy('tasklist')

    def form_valid(self, form):
        form.instance.user =self.request.user
        return super(TaskCreate,self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    template_name= 'task_create.html'
    success_url= reverse_lazy('tasklist')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_delete.html'
    success_url= reverse_lazy('tasklist')

class Logins(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user= True

    def get_success_url(self):
        return reverse_lazy('tasklist')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user= True
    success_url= reverse_lazy('tasklist')

    def form_valid(self, form) :
        user= form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)
    




