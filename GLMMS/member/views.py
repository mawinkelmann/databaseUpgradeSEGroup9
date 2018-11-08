'''The views for the member app.'''
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django import forms
from django.contrib.auth.decorators import login_required
#from django.template import loader 

from django.contrib.auth.models import User
from django.core import serializers
from .models import Profile


class ProfileDetailView(generic.DetailView):
	'''This is a detail view for the a profile'''
	model = Profile
	template_name = 'member/profile.html'

class SingleSearchForm(forms.Form):
	'''Form class for the single search view'''
	#get the data to populate the select forms with
	#create the model fields
	BLANK='----'
	actives_choice = forms.ChoiceField(required=False, choices=Profile.get_all_members_by_category(BLANK)[Profile.ACTIVE], label="Active Members")
	alumni_choice = forms.ChoiceField(required=False, choices=Profile.get_all_members_by_category(BLANK)[Profile.ALUMNI], label="Alumni Members")
	newmembers_choice = forms.ChoiceField(required=False, choices=Profile.get_all_members_by_category(BLANK)[Profile.NEWMEMBER], label="New Members")
	inactives_choice = forms.ChoiceField(required=False, choices=Profile.get_all_members_by_category(BLANK)[Profile.INACTIVE], label="Inactive Members")

	'''this is where to manipulate the forms'''
class MultiSearchForm(forms.Form):
	'''Form class for the multi member search view'''
	#get the data to populate the select forms with
	ALL_MEMBERS = '__all__'
	#create the model fields
	statuses = list(Profile.STATUS)
	statuses.insert(0, (ALL_MEMBERS, 'All Members'))
	status_choice = forms.ChoiceField(required=True, choices=statuses, label="Member Group to Search?")
	#fields to pick which collumns to search and how to sort
	#not in ('bio', 'photo', 'jobs', 'organizations', 'positions', 'pledge_father', 'cell_carrier_id')]
	dict_fields = Profile.get_printable_fields()
	#convert the fields to a list to use it in the choices field.
	fields = []
	for key, value in dict_fields.items():
		fields.append((key, value))
	#fields = [(field.name, field.verbose_name) for field in Profile._meta.get_fields() if not isinstance(field, ManyToOneRel)]
	#multiple choice fields are a multipe select
	fields.insert(0,(ALL_MEMBERS, 'Everything'))
	field_choice = forms.MultipleChoiceField(required=True, choices=fields, label="What information to display?")
	#remove everything option from the ordering cause that doesnt make sense
	fields.remove((ALL_MEMBERS, 'Everything'))
	order_choice = forms.MultipleChoiceField(required=True, choices=fields, label="How to sort the Results?")

class ProfileEditForm(forms.ModelForm):
	'''This class provides a profile edit form.'''
	class Meta:
		model = Profile
		fields = ['bio', 'phone', 'address', 'pledge_class', 'major', 'major2', 'emphasis', 'grad_semester', 'grad_year', 'shirt_size', 'member_status', 'linkedin_profile', 'cumulative_gpa', 'last_sem_gpa', 'last_update', 'birth_date', 'photo', 'pledge_father', 'cell_carrier_id']

class UserEditForm(forms.ModelForm):
	'''THis class provides an edit form for the user.'''
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']

@login_required
def search_index(request):
	'''view returns a rendered template for search_index page'''
	return render(request, 'member/search_index.html')

@login_required
def single_search(request):
	'''View to return a form to search for a member's profile. Handles Get and Post'''
    #handle a search for a profile
	if request.method == 'POST':
		#create a form object from the request
		form = SingleSearchForm(request.POST)
		profile = None
		#validate input
		if form.is_valid():
			#check all the select boxes for a choice that isnt BLANK
			for key in form.cleaned_data:
				if form.cleaned_data[key]:
					#get the profile object sepcified by the user choice.
					profile = Profile.objects.get(pk=int(form.cleaned_data[key]))
					choices = Profile.get_printable_fields()
					#we dont want to show the linked in profile in the table because its in the profile highlight area
					del choices['linkedin_profile']
			if profile is not None:
				return render(request, 'member/single_search.html', {'form': form, 'profile': profile})
			return render(request, 'member/single_search.html', {'form': form, 'error_message': "Please select a member from one of the lists!"})
    #handle a GET request for just the form
	else:
		#empty form
		form = SingleSearchForm()
	#return a page without a profile result
	return render(request, 'member/single_search.html', {'form': form})

@login_required
def edit_info(request, profile_id):
	'''view to return a page to edit a user's profile info. Handles GET and POST'''
	#get the requested profile, or if it cannot be found, return 404
	profile = get_object_or_404(Profile, pk=profile_id)
	#handle a request to edit the info
	if request.method == "POST":
		#create the forms from the user inputted data
		pro_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
		user_form = UserEditForm(request.POST, instance=profile.user)
		#if the forms are valid, save the changes. 
		if pro_form.is_valid() and user_form.is_valid():
			profile = pro_form.save()
			user_form.save()
			#return success message and redirect to profile. 
			#TODO change to a redirect
			return render(request, 'member/profile.html', {'profile': profile, 'error_message': "Changes have been saved!"})
	#handle a reuest for a prepopulated form to edit using the logged in user
	else:
		pro_form = ProfileEditForm(instance=profile)
		user_form = UserEditForm(instance=profile.user)
	return render(request, 'member/member_edit_form.html', {'profile_form': pro_form, 'user_form': user_form})

@login_required
def multi_search(request):
	'''view to handle the GET and POST of the multi search page.'''
	#handle a search form submission
	if request.method == 'POST':
		#create the form from the the user submitted data
		form = MultiSearchForm(request.POST)
		#validate the form
		if form.is_valid():
			#get the choices from the form
			status = form.cleaned_data['status_choice']
			fields = form.cleaned_data['field_choice']
			order = form.cleaned_data['order_choice']
			print(order)
			# get the requested subset of users
			if status == MultiSearchForm.ALL_MEMBERS:
				results = Profile.objects.all()
			else:
				results = Profile.objects.filter(member_status=status)
			#order the results
			for x in order:
				results.order_by(x)
			#get the list of fields the user wanted to see. 
			display_fields = []
			for key in Profile.get_printable_fields().keys():
				if MultiSearchForm.ALL_MEMBERS in fields:
					display_fields.append(key)
				else:
					display_fields = fields
			print(results)
			print(display_fields)
			#have to serialize so we can loop through just these fields in the template 
			data = serializers.serialize( "python", results, fields=display_fields)
			#zip the profiles and the data to iterate over. could not figure out how to access specific items of the serialized object
			# have to put it in a list so that python will evaluate so we can get its length in the template. 
			results = list(zip(results, data))
			return render(request, 'member/multi_search.html', {'form': form, 'results': results, 'fields': display_fields}) 
	#return an empty form
	else:
		form = MultiSearchForm()
	return render(request, 'member/multi_search.html', {'form': form})

#TODO
@login_required
def position_search(request):
	return render(request, 'member/search_index.html')
#TODO
@login_required
def job_search(request):
	return render(request, 'member/search_index.html')
#TODO
@login_required
def org_search(request):
	return render(request, 'member/search_index.html')
	

