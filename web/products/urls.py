from django.urls import path
from . import views
from . import solve


urlpatterns = [
    path('your_portfolio', views.portfolio, name="your_portfolio"),
    path('report', solve.func1 , name ="report")
]