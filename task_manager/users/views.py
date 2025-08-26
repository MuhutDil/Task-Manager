from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.custom_mixins import CustomUserPassesTestMixin

from .forms import (
    CustomUserCreationForm,
    CustomUserLoginForm,
    CustomUserUpdateForm,
)
from .models import CustomUser


class UserBaseViewMixin(CustomUserPassesTestMixin):
    model = CustomUser
    context_object_name = "user"
    success_url = reverse_lazy("users_list")
    success_message = ''
    error_permission_message = (
        _("You do not have permission to modify another user.")
    )
    error_redirect = reverse_lazy("users_list")
    
    def test_func(self):
        profile = self.get_object()
        return profile == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "users/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("User registered successfully."))
        return response


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = CustomUserLoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("You are logged in."))
        return response


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(self.request, _("You are logged out."))
        return super().dispatch(request, *args, **kwargs)


class UserListView(ListView):
    model = CustomUser
    template_name = "users/list.html"
    context_object_name = "users"
    ordering = ["id"]


class UserUpdateView(UserBaseViewMixin, UpdateView):
    form_class = CustomUserUpdateForm
    template_name = "update.html"
    extra_context = {'title': _('Update user data')}
    success_message = _("User successfully updated.")


class UserDeleteView(UserBaseViewMixin, DeleteView):
    template_name = "delete.html"
    extra_context = {'title': _('Deleting user')}
    success_message = _("User successfully deleted.")
    error_message = _("Cannot delete user because it is in use.")

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request, self.error_message
            )
            return redirect(self.success_url)