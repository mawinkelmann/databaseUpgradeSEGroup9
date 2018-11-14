from django import forms
from django.contrib.auth.models import User

from .models import Profile

class SingleSearchForm(forms.Form):
	'''Form class for the single search view'''
	#get the data to populate the select forms with
	#create the model fields
	actives_choice = forms.ChoiceField(required=False, choices=[], label="Active Members")
	alumni_choice = forms.ChoiceField(required=False, choices=[], label="Alumni Members")
	newmembers_choice = forms.ChoiceField(required=False, choices=[], label="New Members")
	inactives_choice = forms.ChoiceField(required=False, choices=[], label="Inactive Members")
	def __init__(self, *args, **kwargs):
		super(SingleSearchForm, self).__init__(*args, **kwargs)
		BLANK='----'
		members = Profile.get_all_members_by_category(BLANK)
		self.fields['actives_choice'] = forms.ChoiceField(required=False, choices=members[Profile.ACTIVE], label="Active Members")
		self.fields['alumni_choice'] = forms.ChoiceField(required=False, choices=members[Profile.ALUMNI], label="Alumni Members")
		self.fields['newmembers_choice'] = forms.ChoiceField(required=False, choices=members[Profile.NEWMEMBER], label="New Members Members")
		self.fields['inactives_choice'] = forms.ChoiceField(required=False, choices=members[Profile.INACTIVE], label="Inactive Members")
	
class MultiSearchForm(forms.Form):
	'''Form class for the multi member search view'''
	#get the data to populate the select forms with
	#create the model fields
	status_choice = forms.ChoiceField()
	#fields = [(field.name, field.verbose_name) for field in Profile._meta.get_fields() if not isinstance(field, ManyToOneRel)]
	field_choice = forms.MultipleChoiceField()
	order_choice = forms.MultipleChoiceField()
	ALL_MEMBERS = '__all__'
	def __init__(self, *args, **kwargs):
		super(MultiSearchForm, self).__init__(*args, **kwargs)
		#fields to pick which collumns to search and how to sort
		#not in ('bio', 'photo', 'jobs', 'organizations', 'positions', 'pledge_father', 'cell_carrier_id')]
		dict_fields = Profile.get_printable_fields()
		fields = []
		for key, value in dict_fields.items():
			fields.append((key, value))
		statuses = list(Profile.STATUS)
		statuses.insert(0, (MultiSearchForm.ALL_MEMBERS, 'All Members'))
		self.fields['status_choice'] = forms.ChoiceField(required=True, choices=statuses, initial={MultiSearchForm.ALL_MEMBERS: 'Everything'}, label="Member Group to Search?")
		#multiple choice fields are a multipe select
		fields.insert(0,(MultiSearchForm.ALL_MEMBERS, 'Everything'))
		self.fields['field_choice'] = forms.MultipleChoiceField(required=True, choices=fields, initial=MultiSearchForm.ALL_MEMBERS, label="What information to display?")
		#remove everything option from the ordering cause that doesnt make sense
		fields.remove((MultiSearchForm.ALL_MEMBERS, 'Everything'))
		fields.insert(0,('user__username', 'Username'))
		fields.insert(1,('user__last_name', 'Last Name'))
		fields.insert(2,('user__first_name', 'First Name'))
		self.fields['order_choice'] = forms.MultipleChoiceField(required=True, choices=fields, initial='user__username', label="How to sort the results?")

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