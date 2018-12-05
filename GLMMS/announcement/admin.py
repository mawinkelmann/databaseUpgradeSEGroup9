from django.contrib import admin

from announcement.models import Announcement, Comment

# Register your models here.
admin.site.register(Announcement)
admin.site.register(Comment)
