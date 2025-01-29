from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from users.models import CustomUser
from users.forms import CustomUserCreationForm


# Create your views here.
class Success(TemplateView):
    template_name = "success.html"


class CreateUser(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "user_creation.html"

    success_url = reverse_lazy("users:success")


class UpdateUser(UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "user_creation.html"

    success_url = reverse_lazy("users:success")


class DeleteUser(DeleteView):
    model = CustomUser

    success_url = reverse_lazy("users:success")
