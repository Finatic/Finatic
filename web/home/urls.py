from django.urls import path
from . import views


urlpatterns = [
    path('about', views.about, name="about"),
    path('', views.home, name="home"),
    path('result', views.result, name="result"),
    path('contact', views.contact_us, name="contact"),
    path('Portfolio_Optimization', views.Portfolio_Optimization,
         name="Portfolio_Optimization"),
]
