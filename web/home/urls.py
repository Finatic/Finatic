from django.urls import path
from . import views


urlpatterns = [
    path('about', views.about, name="about"),
    path('', views.home, name="home"),
    path('try', views.result, name="result"),
    path('contact', views.contact_us, name="contact"),
    path('Portfolio_Optimiser/Portfolio_Optimization.html', views.Portfolio_Optimization,
         name="Portfolio_Optimization"),
]
