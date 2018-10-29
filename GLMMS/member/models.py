import datetime

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
'''
id int NOT NULL AUTO_INCREMENT,
phone varchar(14),
cell_carrier_id int,
address varchar(255),
pledge_class varchar(31),
major varchar(63),
major2 varchar(63),
pledge_father_pawprint varchar(6),
grad_semester varchar(5),
grad_year varchar(4),
shirt_size ENUM('M', 'XS', 'S', 'L', 'XL', 'XXL', 'XXXL'),
current_job_id int,
status ENUM('Active', 'Alumni', 'Inactive'),
cumulative_gpa float,
last_sem_gpa float,
emphasis varchar(63),
last_update Date,
photo_path VARCHAR(255),
linkedin_profile VARCHAR(255),
last_random_pic_date Date,
PRIMARY KEY(id),
KEY `fk_father_pawprint` (`pledge_father_pawprint`),
CONSTRAINT `fk_father_pawprint` FOREIGN KEY (`pledge_father_pawprint`) REFERENCES `all_members` (`pawprint`),
FOREIGN KEY(pawprint) REFERENCES authentication(username)
'''

def gen_file_path(instance, filename):
	return 'images/profile_pics/{0}_{1}'.format(instance.user.username, filename)

#doc for user model here https://docs.djangoproject.com/en/2.1/ref/contrib/auth/
class Profile(models.Model):
	#Note: User.username should be the user's pawprint
	#enums
	FALL = 'F'
	SPRING = 'S'
	ACTIVE = 'A'
	ALUMNI = 'B'
	INACTIVE = 'C'
	SHIRTSIZE = (('M', 'Medium'), ('XS', 'Extra Small'), ('S', 'Small'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Double XL'), ('XXXL', 'Triple XL'),)
	SEMESTERS = ((SPRING, 'Spring'), (FALL, 'Fall'),)
	STATUS = ((ACTIVE, 'Active'), (ALUMNI, 'Alumni'), (INACTIVE, 'Inactive'),)
	#collumns
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	phone = models.CharField("phone number", max_length=14, blank=True)
	address = models.CharField(max_length=255, blank=True)
	pledge_class = models.CharField(max_length=31, blank=True)
	major = models.CharField("decalared major", max_length=63, blank=True)
	major2 = models.CharField("second major", max_length=63, blank=True)
	emphasis = models.CharField(max_length=63, blank=True)
	grad_semester = models.CharField("semester graduating", max_length=1, choices=SHIRTSIZE, blank=True)
	grad_year = models.CharField("year graduating", max_length=4, blank=True)
	shirt_size = models.CharField(max_length=4, choices=SHIRTSIZE, blank=True)
	member_status = models.CharField(max_length=1, choices=STATUS, blank=True)
	linkedin_profile = models.URLField(max_length=255, blank=True)
	cumulative_gpa = models.FloatField('cumulative GPA', blank=True)
	last_sem_gpa = models.FloatField('last semester GPA', blank=True)
	last_update = models.DateField(null=True, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	photo = models.ImageField(upload_to=gen_file_path)
	last_random_pic_date =  models.DateField(null=True, blank=True)
	pledge_father_pawprint = models.ForeignKey(User, on_delete=models.CASCADE)
	cell_carrier_id = models.ForeignKey(Cell_Carriers, on_delete=models.CASCADE)
	positions = models.ManyToManyField(Position, through='Position_History')
	organizations = models.ManyToManyField(Organization, through='Organization_Involvement')
	jobs = models.ManyToManyField(Companies, through='Job_History')
	
	
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Job_History(model.Model):
	#define the Job_History class here
	pass
	
class Position_History(model.Model):
	#define the Position_History class here
	pass
	
class Organization_Involvement(model.Model):
	#define the Organization_Involvement class here
	pass
	
class Companies(model.Model):
	#define the Companies class here
	pass

class Position(model.Model):
	#define the position class here
	pass
	
class Organizations(model.Model):
	#define the Organizations class here
	pass
	
class Cell_Carriers(model.Models):
	#define the cell carriers table here
	pass
	
