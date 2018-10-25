from django.db import models

# Create your models here.
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Member(models.Model):
    """Model representing a member."""
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
