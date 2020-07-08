from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs):
	print(request.user)
	return render(request, "home.html", {})

def team_view(request, *args, **kwargs):
	print(request.user)
	return render(request, "team.html", {})

def about_view(request, *args, **kwargs):
	print(request.user)
	return render(request, "about.html", {})

	
def base(request):
	return render(request,'base.html')

