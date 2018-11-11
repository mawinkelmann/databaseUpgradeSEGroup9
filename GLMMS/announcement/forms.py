from django import forms
from django.contrib.auth.models import User

from .models import Announcement

class AnnouncementForm(forms.ModelForm):
	'''This class provides an announcement creation form.'''
	class Meta:
		model = Announcement
		fields = ['type', 'topic', 'title', 'message']
