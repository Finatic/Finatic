from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def result_view(request, *args, **kwargs):
	context = {
		'a':'Heloo'
	}
	return render(request, "result.html", context)