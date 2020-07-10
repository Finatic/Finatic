from django.urls import path
from . import views
from .views import register_user, edit_user, password_change
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_user.as_view(), name='register'),
    path('edit_profile/', edit_user.as_view(), name='edit_profile'),
    path('password/', password_change.as_view(), name='password_change'),


    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="registration/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="registration/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset123/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="registration/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="registration/password_reset_done.html"),
         name="password_reset_complete"),

]
