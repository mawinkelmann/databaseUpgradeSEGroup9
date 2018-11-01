from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django import forms
#from django.template import loader 

from django.contrib.auth.models import User
from django.core import serializers
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

	
class MultiSearchForm(forms.Form):
	from django.db.models import ManyToOneRel
	#get the data to populate the select forms with
	#values('fieldname')
	ALL_MEMBERS = '__all__'
	#create the model fields
	#choice field of member status types
	statuses = list(Profile.STATUS)
	statuses.insert(0, (ALL_MEMBERS, 'All Members'))
	status_choice = forms.ChoiceField(required=True, choices=statuses, label="Member Group to Search?")
	#fields to pick which collumns to search and how to sort
	#not in ('bio', 'photo', 'jobs', 'organizations', 'positions', 'pledge_father', 'cell_carrier_id')]
	dict_fields = Profile.get_printable_fields()
	fields = []
	for key, value in dict_fields.items():
		fields.append((key, value))
	#fields = [(field.name, field.verbose_name) for field in Profile._meta.get_fields() if not isinstance(field, ManyToOneRel)]
	fields.insert(0,(ALL_MEMBERS, 'Everything'))
	field_choice = forms.MultipleChoiceField(required=True, choices=fields, label="What information to display?")
	fields.remove((ALL_MEMBERS, 'Everything'))
	order_choice = forms.MultipleChoiceField(required=True, choices=fields, label="How to sort the Results?")

class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['bio', 'phone', 'address', 'pledge_class', 'major', 'major2', 'emphasis', 'grad_semester', 'grad_year', 'shirt_size', 'member_status', 'linkedin_profile', 'cumulative_gpa', 'last_sem_gpa', 'last_update', 'birth_date', 'photo', 'pledge_father', 'cell_carrier_id']

class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']


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
                    choices = Profile.get_printable_fields()
                    del choices['linkedin_profile']
                    data = serializers.serialize( "python", [profile], fields=choices)
            if profile is not None:
                return render(request, 'member/single_search.html', {'form': form, 'profile': profile, 'data': data})
            return render(request, 'member/single_search.html', {'form': form, 'error_message': "Please select a member from one of the lists!"})
    else:
        form = SingleSearchForm()
    return render(request, 'member/single_search.html', {'form': form})

def edit_info(request, profile_id):
	profile = get_object_or_404(Profile, pk=profile_id)
	if request.method == "POST":
		pro_form = ProfileEditForm(request.POST, instance=profile)
		user_form = UserEditForm(request.POST, instance=profile.user)
		if pro_form.is_valid() and user_form.is_valid():
			profile = form.save()
			user_form.save()
			#return HttpResponseRedirect(reverse('member:profile', args=(question.id,)))
			return render(request, 'member/profile.html', {'profile': profile, 'error_message': "Changes have been saved!"})
	else:
		pro_form = ProfileEditForm(instance=profile)
		user_form = UserEditForm(instance=profile.user)
	return render(request, 'member/member_edit_form.html', {'profile_form': pro_form, 'user_form': user_form})

def multi_search(request):
	if request.method == 'POST':
		form = MultiSearchForm(request.POST)
		if form.is_valid():
			status = form.cleaned_data['status_choice']
			fields = form.cleaned_data['field_choice']
			order = form.cleaned_data['order_choice']
			print(order)
			if status == MultiSearchForm.ALL_MEMBERS:
				results = Profile.objects.all()
			else:
				results = Profile.objects.filter(member_status=status)
			for x in order:
				results.order_by(x)
			display_fields = []
			for key in Profile.get_printable_fields().keys():
				if MultiSearchForm.ALL_MEMBERS in fields:
					display_fields.append(key)
				else:
					display_fields = fields
			print(results)
			print(display_fields)
			from django.core import serializers
			data = serializers.serialize( "python", results, fields=display_fields)
			#zip the profiles and the data to iterate over. could not figure out how to access specific items of the serivalized object
			results = list(zip(results, data))
			return render(request, 'member/multi_search.html', {'form': form, 'results': results, 'fields': display_fields}) 
	else:
		form = MultiSearchForm()
	return render(request, 'member/multi_search.html', {'form': form})
	
def position_search(request):
	return render(request, 'member/search_index.html')
	
def job_search(request):
	return render(request, 'member/search_index.html')
	
def org_search(request):
	return render(request, 'member/search_index.html')
	

