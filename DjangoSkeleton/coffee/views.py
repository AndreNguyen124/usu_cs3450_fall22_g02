from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# from .models import custom_function


def index(request):
	return render(request, 'coffee/index.html')
	
	
	
	
	