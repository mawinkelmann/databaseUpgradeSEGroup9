from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
#from django.template import loader 

from .models import Profile

class SingleDetailView(generic.DetailView):
	model = Profile
	template_name = 'member/single_detail.html'
	
def search_index(request):
	return render(request, 'member/search_index.html')
	
def single_search(request):
	return render(request, 'member/search_index.html')
	
def multi_search(request):
	return render(request, 'member/search_index.html')
	
def position_search(request):
	return render(request, 'member/search_index.html')
	
def job_search(request):
	return render(request, 'member/search_index.html')
	
def org_search(request):
	return render(request, 'member/search_index.html')
	

