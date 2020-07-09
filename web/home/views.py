from django.shortcuts import render

# Create your views here.
def home(request, ):
	return render(request, "home.html")

def team(request):
	return render(request, "team.html")

def about(request):
	return render(request, "about.html")

	
def base(request):
	return render(request,'base.html')

def result(request, ):
	return render(request, "result.html")
	
