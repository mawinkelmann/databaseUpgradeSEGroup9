from django import forms
from django.contrib.auth.models import User

from .models import Announcement, Comment

class AnnouncementForm(forms.ModelForm):
	'''This class provides an announcement creation form.'''
	class Meta:
		model = Announcement
		fields = ['type', 'topic', 'title', 'message']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text',]
