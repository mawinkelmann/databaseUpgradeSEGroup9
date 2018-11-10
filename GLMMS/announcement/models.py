from django.db import models
from django.conf import settings
import datetime

from member.models import Profile
# Create your models here.
class Announcement(models.Model):
	GENERAL = 'A'
	SOCIAL = 'B'
	PROFESSIONAL = 'C'
	PHILANTHROPY = 'D'
	RECRUITMENT = 'E'
	NEWMEMBER = 'F'
	NORMAL = 'G'
	URGENT = 'H'
	TYPES = ((NORMAL, 'Normal'), (URGENT, 'Urgent'),)
	TOPICS = ((GENERAL, 'General'), (SOCIAL,'Social'), (PROFESSIONAL, 'Professional'), (PHILANTHROPY, 'Philanthropy'), (RECRUITMENT, 'Recruitment'), (NEWMEMBER, 'New Member'),)
										#Profile
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=63)
	topic = models.CharField(max_length=1, choices=TOPICS, default=GENERAL)
	type = models.CharField(max_length=1, choices=TYPES, default=NORMAL)
	message = models.TextField()
	dateAdded = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title
