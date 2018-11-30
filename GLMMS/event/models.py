from django.db import models
from django.conf import settings
import datetime

from member.models import Profile
# Create your models here.
class Event(models.Model):
	GENERAL = 'A'
	SOCIAL = 'B'
	PROFESSIONAL = 'C'
	PHILANTHROPY = 'D'
	RECRUITMENT = 'E'
	NEWMEMBER = 'F'
	BROTHERHOOD = 'G'
	TOPICS = ((GENERAL, 'General'), (SOCIAL,'Social'), (PROFESSIONAL, 'Professional'), (PHILANTHROPY, 'Philanthropy'), (RECRUITMENT, 'Recruitment'), (NEWMEMBER, 'New Member'), (BROTHERHOOD,'Brotherhood Development'),)										#Profile
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=63)
	topic = models.CharField(max_length=1, choices=TOPICS, default=GENERAL)
	is_public = models.BooleanField(default=False)
	description = models.TextField()
	address = models.CharField(max_length=127)
	city = models.CharField(max_length=31)
	state = models.CharField(max_length=15)
	zipcode = models.CharField(max_length=5)
	dateAdded = models.DateTimeField(auto_now_add=True)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	rsvps = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Event_RSVPs', related_name='member_rsvps')

	def __str__(self):
		return self.title

class Event_RSVPs(models.Model):
	'''table for the relation of profiles to orgs'''
	member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
