from django.urls import path
from . import views


urlpatterns = [
    path('your_portfolio', views.portfolio, name="your_portfolio"),
    path('submit', views.solve, name ="res")
]