from django.urls import path
from . import views


urlpatterns = [
    path('your_portpolio', views.portfolio, name="portfolio"),
    path('submit', views.solve, name ="res")
]