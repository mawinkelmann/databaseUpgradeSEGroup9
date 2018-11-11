from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpRequest, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django import forms

from .models import Announcement

# Create your views here.


def AnnouncementsView(request):

    announcements = Announcement.objects.order_by('-dateAdded')
    return render(request, 'announcement/announcement_view_all.html', {'announcements': announcements})
