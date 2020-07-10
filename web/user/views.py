from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from .forms import register, edit, change_password
from django.contrib.auth.views import PasswordChangeView


class register_user(generic.CreateView):
    form_class = register
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class edit_user(generic.UpdateView):
    form_class = edit
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


class password_change(PasswordChangeView):
    form_class = change_password
    template_name = 'registration/change-password.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
