from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.custom_mixins import (
    CustomLoginRequiredMixin,
    CustomUserPassesTestMixin,
)

from .filter import TaskFilter
from .forms import TaskChangeForm, TaskCreationForm
from .models import Task


class TaskBaseViewMixin(CustomLoginRequiredMixin):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("tasks_list")
    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class TaskListView(TaskBaseViewMixin, FilterView):
    filterset_class = TaskFilter
    template_name = "tasks/list.html"
    context_object_name = "tasks"
    ordering = ["id"]


class TaskCreateView(TaskBaseViewMixin, CreateView):
    form_class = TaskCreationForm
    template_name = "create.html"
    extra_context = {'title': _('Create task')}
    success_message = _("Task successfully created.")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(TaskBaseViewMixin, DetailView):
    template_name = "tasks/detail.html"


class TaskUpdateView(TaskBaseViewMixin, UpdateView):
    form_class = TaskChangeForm
    template_name = "update.html"
    extra_context = {'title': _('Change task')}
    success_message = _("Task successfully updated.")


class TaskDeleteView(CustomUserPassesTestMixin, TaskBaseViewMixin, DeleteView):
    template_name = "delete.html"
    extra_context = {'title': _('Delete task')}
    success_message = _("Task successfully deleted.")
    error_permission_message = _("Task can only be deleted by its author.")
    error_redirect = reverse_lazy("tasks_list")

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user

