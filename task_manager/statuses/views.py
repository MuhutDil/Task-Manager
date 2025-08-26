from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.custom_mixins import CustomLoginRequiredMixin

from .forms import StatusChangeForm, StatusCreationForm
from .models import Status


class StatusBaseViewMixin(CustomLoginRequiredMixin):
    model = Status
    context_object_name = "status"
    success_url = reverse_lazy("statuses_list")
    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class StatusListView(StatusBaseViewMixin, ListView):
    template_name = "statuses/list.html"
    context_object_name = "statuses"
    ordering = ["id"]


class StatusCreateView(StatusBaseViewMixin, CreateView):
    form_class = StatusCreationForm
    template_name = "create.html"
    extra_context = {'title': _('Create status')}
    success_message = _("Status successfully created.")


class StatusUpdateView(StatusBaseViewMixin, UpdateView):
    form_class = StatusChangeForm
    template_name = "update.html"
    extra_context = {'title': _('Change status')}
    success_message = _("Status successfully updated.")


class StatusDeleteView(StatusBaseViewMixin, DeleteView):
    template_name = "delete.html"
    extra_context = {'title': _('Delete status')}
    success_message = _("Status successfully deleted.")
    error_message = _("Cannot delete status because it is in use.")

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request, self.error_message
            )
            return redirect(self.success_url)
            