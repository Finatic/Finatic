from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs):
	context ={}
	return render(request, "home.html", context)

def team_view(request, *args, **kwargs):
	context = {}
	return render(request, "team.html", context)

def about_view(request, *args, **kwargs):
	print(request.user)
	return render(request, "about.html", {})

	
def base(request):
	return render(request,'base.html')

	
