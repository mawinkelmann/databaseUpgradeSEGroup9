'''this file defines the models of the member application'''
import datetime

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

FALL = 'F'
SPRING = 'S'
SEMESTERS = ((SPRING, 'Spring'), (FALL, 'Fall'),)

class Company(models.Model):
	'''Model defining the company table. It keeps track of companies members have worked for'''
	company_name = models.CharField(max_length=63)
	def __str__(self):
		return self.company_name

class Position(models.Model):
	'''The Model to define the Position table. This contains all available positions a member can hold'''
	APPOINTED = 'A'
	ELECTED = 'B'
	EXEC = 'C'
	TYPES = ((APPOINTED, 'Appointed'), (ELECTED, 'Elected'), (EXEC, 'Executive Board'),)
	title = models.CharField(max_length=63)
	type = models.CharField(max_length=1, choices=TYPES)
	def __str__(self):
		return self.title
	
class Organization(models.Model):
	'''Model defining the organizations table. It keeps track of orgs members are involved in.'''
	name = models.CharField(max_length=63)
	def __str__(self):
		return self.name
	
class Cell_Carrier(models.Model):
	'''table to define the list of cell carriers so they can be mapped to an SMS gateway address'''
	name = models.CharField(max_length=63)
	sms_address = models.CharField("SMS Email Gateway", max_length=63)
	
	def __str__(self):
		return self.name
	
class Job_History(models.Model):
	'''Table relating companies to profiles'''
	member = models.ForeignKey('Profile', on_delete=models.CASCADE)
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	title = models.CharField(max_length=63)
	state = models.CharField(max_length=31)
	city = models.CharField(max_length=31)
	start_date = models.DateField()
	end_date = models.DateField(null=True, blank=True)
	
class Position_History(models.Model):
	'''table relating positions to profiles'''
	member = models.ForeignKey('Profile', on_delete=models.CASCADE)
	position = models.ForeignKey(Position, on_delete=models.CASCADE)
	semester = models.CharField(max_length=1, choices=SEMESTERS)
	year = models.CharField(max_length=4)
	
class Organization_Involvement(models.Model):
	'''table for the relation of profiles to orgs'''
	member = models.ForeignKey('Profile', on_delete=models.CASCADE)
	company = models.ForeignKey(Organization, on_delete=models.CASCADE)
	position = models.CharField(max_length=63)

def gen_file_path(instance, filename):
	'''returns a path to save a profile picture for the profile object. it will be loctaed relative to the MEDIA_ROOT defined in setting.py'''
	return 'profile_pics/{0}_{1}'.format(instance.user.username, filename)

#models are given an id pk field automatically 
#doc for user model here https://docs.djangoproject.com/en/2.1/ref/contrib/auth/
class Profile(models.Model):
	'''This is the class holding additional information about each user. Has a one-to-one rel to Django defined User'''
	#Note: User.username should be the user's pawprint
	#enums
	ACTIVE = 'A'
	ALUMNI = 'B'
	INACTIVE = 'C'
	NEWMEMBER = 'D'
	SHIRTSIZE = (('M', 'Medium'), ('XS', 'Extra Small'), ('S', 'Small'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Double XL'), ('XXXL', 'Triple XL'),)
	STATUS = ((ACTIVE, 'Active'), (ALUMNI, 'Alumni'), (INACTIVE, 'Inactive'), (NEWMEMBER, 'New Member'),)
	#collumns
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	phone = models.CharField("phone number", max_length=14, blank=True)
	address = models.CharField(max_length=255, blank=True)
	pledge_class = models.CharField(max_length=31, blank=True)
	major = models.CharField("declared major", max_length=63, blank=True)
	major2 = models.CharField("second major", max_length=63, blank=True)
	emphasis = models.CharField(max_length=63, blank=True)
	grad_semester = models.CharField("semester graduating", max_length=1, choices=SEMESTERS, blank=True)
	grad_year = models.CharField("year graduating", max_length=4, blank=True)
	shirt_size = models.CharField(max_length=4, choices=SHIRTSIZE, blank=True)
	member_status = models.CharField(max_length=1, choices=STATUS, blank=True)
	linkedin_profile = models.URLField(max_length=255, blank=True)
	cumulative_gpa = models.FloatField('cumulative GPA', blank=True, null=True)
	last_sem_gpa = models.FloatField('last semester GPA', blank=True, null=True)
	last_update = models.DateField(null=True, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	photo = models.ImageField(upload_to=gen_file_path, blank=True)
	last_random_pic_date =  models.DateField(null=True, blank=True)
	pledge_father = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
	cell_carrier_id = models.ForeignKey(Cell_Carrier, on_delete=models.CASCADE, null=True)
	positions = models.ManyToManyField(Position, through='Position_History')
	organizations = models.ManyToManyField(Organization, through='Organization_Involvement')
	jobs = models.ManyToManyField(Company, through='Job_History')

	def __str__(self):
		return "{0}: {1} {2}".format(self.user.username, self.user.first_name, self.user.last_name)
	
	#we dont want to display linkedin_profile, photo, bio, 
	#cell carrier id and user id need some work. 
	#only display gpa if the member calling it is the user
	@staticmethod
	def get_printable_fields():
		'''return a dict of fields[field.name] = field.verbose_name. ie keys= field names and values = verbose field names'''
		fields = {}
		for field in Profile._meta.get_fields():
			if field.name not in ('user', 'bio', 'photo', 'jobs', 'organizations', 'positions', 'pledge_father', 'cell_carrier_id', 'id'):
				try:
					fields[field.name] = field.verbose_name
				except AttributeError:
					pass
		#fields = [(field.verbose_name, field.value_to_string(self)) for field in Profile._meta.fields if field.verbose_name not in ('bio', 'photo','linkedin profile')]
		return fields

	def get_printable_fields_and_values(self):
		'''returns a list of (verbose_name,value to string) for each field of this profile instance'''
		fields = [(field.verbose_name, field.value_to_string(self)) for field in Profile._meta.fields if field.verbose_name not in ('ID','user','bio', 'photo','linkedin profile','pledge father', 'cell carrier id',)]
		return fields

	@staticmethod
	def get_all_members_by_category(blank):
		'''returns a dict of {category: [(profile.id, str(profile))]}'''
		choices = {Profile.ACTIVE: None, Profile.ALUMNI: None, Profile.NEWMEMBER: None, Profile.INACTIVE: None}
		for key in choices:
			choices[key] = [(profile.id, str(profile)) for profile in Profile.objects.filter(member_status=key).order_by('user__username')]
			choices[key].append(('', blank))
		print(choices)
		return choices

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	'''catch the creation of a user and make a profile for them too'''
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	'''catch the save of a user and save the profile too.'''
	instance.profile.save()

	

	
