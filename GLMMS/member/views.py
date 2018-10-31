from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django import forms
#from django.template import loader 

from .models import Profile

class ProfileDetailView(generic.DetailView):
	model = Profile
	template_name = 'member/profile.html'
	
class SingleSearchForm(forms.Form):
	#get the data to populate the select forms with
	#values('fieldname')
	BLANK='----'
	choices = {Profile.ACTIVE: None, Profile.ALUMNI: None, Profile.NEWMEMBER: None, Profile.INACTIVE: None}
	for key in choices:
		choices[key] = [(profile.id, str(profile)) for profile in Profile.objects.filter(member_status=key).order_by('user__username')]
		choices[key].append(('', BLANK))
	'''alumni = [(str(profile),profile.id) for profile in Profile.objects.filter(member_status=Profile.ALUMNI).order_by('user__username')]
	newmembers = [(str(profile),profile.id) for profile in Profile.objects.filter(member_status=Profile.NEWMEMBER).order_by('user__username')]
	inactives = [(str(profile), profile.id) for profile in Profile.objects.filter(member_status=Profile.INACTIVE).order_by('user__username')]'''
	print(choices[Profile.ACTIVE])
	#create the model fields
	actives_choice = forms.ChoiceField(required=False, choices=choices[Profile.ACTIVE], label="Active Members")
	alumni_choice = forms.ChoiceField(required=False, choices=choices[Profile.ALUMNI], label="Alumni Members")
	newmembers_choice = forms.ChoiceField(required=False, choices=choices[Profile.NEWMEMBER], label="New Members")
	inactives_choice = forms.ChoiceField(required=False, choices=choices[Profile.INACTIVE], label="Inactive Members")

class MemberEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['bio', 'phone', 'address', 'pledge_class', 'major', 'major2', 'emphasis', 'grad_semester', 'grad_year', 'shirt_size', 'member_status', 'linkedin_profile', 'cumulative_gpa', 'last_sem_gpa', 'last_update', 'birth_date', 'photo', 'pledge_father', 'cell_carrier_id']

def search_index(request):
	return render(request, 'member/search_index.html')
	
def single_search(request):
	if request.method == 'POST':
		form = SingleSearchForm(request.POST)
		profile = None
		if form.is_valid():
			for key in form.cleaned_data:
				if form.cleaned_data[key]:
					profile = Profile.objects.get(pk=int(form.cleaned_data[key]))
			if profile is not None:
				return render(request, 'member/single_search.html', {'form': form, 'profile': profile})
			else:
				return render(request, 'member/single_search.html', {'form': form, 'error_message': "Please select a member from one of the lists!"})
				#raise forms.ValidationError("Please select a member form one of the lists!")
	else:
		form = SingleSearchForm()
	return render(request, 'member/single_search.html', {'form': form})
	
def edit_info(request, profile_id):
	profile = get_object_or_404(Profile, pk=profile_id)
	if request.method == "POST":
		form = MemberEditForm(request.POST, instance=profile)
		if form.is_valid():
			profile = form.save()
			return render(request, 'member/profile.html', {'profile': profile, 'error_message': "Changes have been saved!"})
	else:
		form = MemberEditForm(instance=profile)
	return render(request, 'member/member_edit_form.html', {'form': form})

def multi_search(request):
	return render(request, 'member/search_index.html')
	
def position_search(request):
	return render(request, 'member/search_index.html')
	
def job_search(request):
	return render(request, 'member/search_index.html')
	
def org_search(request):
	return render(request, 'member/search_index.html')
	

