from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.custom_mixins import CustomLoginRequiredMixin

from .forms import LabelChangeForm, LabelCreationForm
from .models import Label


class LabelBaseViewMixin(CustomLoginRequiredMixin):
    model = Label
    context_object_name = "label"
    success_url = reverse_lazy("labels_list")
    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class LabelListView(LabelBaseViewMixin, ListView):
    template_name = "labels/list.html"
    context_object_name = "labels"
    ordering = ["id"]


class LabelCreateView(LabelBaseViewMixin, CreateView):
    form_class = LabelCreationForm
    template_name = "create.html"
    extra_context = {'title': _('Create label')}
    success_message = _("Label successfully created.")


class LabelUpdateView(LabelBaseViewMixin, UpdateView):
    form_class = LabelChangeForm
    template_name = "update.html"
    extra_context = {'title': _('Change label')}
    success_message = _("Label successfully updated.")


class LabelDeleteView(LabelBaseViewMixin, DeleteView):
    template_name = "delete.html"
    extra_context = {'title': _('Delete label')}
    success_message = _("Label successfully deleted.")
    error_message = _("Cannot delete label because it is in use.")

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request, self.error_message
            )
            return redirect(self.success_url)