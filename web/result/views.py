from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import outputa
from .serializers import outputSerializer

class datalist(APIView):

	def get(self, request):
		data = outputa.objects.all()
		serializer = outputSerializer(data, many=True)
		return Response(serializer.data)

	def post(self):
		pass



# Create your views here.
def result_view(request, *args, **kwargs):
	context = {
		'a':'Heloo'
	}
	return render(request, "result.html", context)
