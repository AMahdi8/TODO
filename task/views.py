from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import *
from .forms import *

# views.py
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from .models import Tasks, Category
from django.contrib.auth.mixins import LoginRequiredMixin


class TasksList(LoginRequiredMixin, ListView):
    model = Tasks
    context_object_name = 'tasks'
    template_name = 'task/tasks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['categories'] = Category.objects.filter(user=self.request.user)

        category_id = self.request.GET.get('category')
        search = self.request.GET.get('search')
        priority = self.request.GET.get('priority')
        is_completed = self.request.GET.get('is_completed')

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            context['tasks'] = context['tasks'].filter(category=category)
            context['selected_category'] = category

        if search:
            context['search'] = search
            context['tasks'] = context['tasks'].filter(title__icontains=search)

        if priority:
            context['priority'] = priority
            context['tasks'] = context['tasks'].filter(priority=priority)

        if is_completed:
            context['is_completed'] = is_completed
            is_completed_bool = is_completed.lower() == 'true'
            context['tasks'] = context['tasks'].filter(
                is_completed=is_completed_bool)

        context['count'] = context['tasks'].count()
        for i in range(len(context['tasks'])):
            context['tasks'][i].description = context['tasks'][i].description[:20]
        context['absolute_url'] = self.request.build_absolute_uri()
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Tasks
    context_object_name = 'task'
    template_name = 'task/task.html'

    def get_context_data(self, **kwargs):
        user_tasks = Tasks.objects.filter(user=self.request.user)
        if kwargs['object'] in user_tasks:
            return super().get_context_data(**kwargs)


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Tasks
    form_class = TaskCreateForm
    template_name = 'task/create.html'
    success_url = reverse_lazy('tasks')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(
            user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create'] = True
        return context


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Tasks
    fields = ['title', 'description', 'priority', 'is_completed', 'category']
    template_name = 'task/create.html'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

    def get_object(self, queryset=None):
        task = super().get_object(queryset)
        if task.user != self.request.user:
            raise PermissionDenied()
        return task


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Tasks
    context_object_name = 'task'
    template_name = 'task/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

    def get_object(self, queryset=None):
        task = super().get_object(queryset)
        if task.user != self.request.user:
            raise PermissionDenied()
        return task


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    context_object_name = 'category'
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

    def get_object(self, queryset=None):
        category = super().get_object(queryset)
        if category.user != self.request.user:
            raise PermissionDenied()
        return category


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = context['categories'].filter(
            user=self.request.user)
        return context
