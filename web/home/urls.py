from django.urls import path
from . import views


urlpatterns = [
    path('',views.base, name="base"),
     path('about',views.about_view, name="about"),  
]