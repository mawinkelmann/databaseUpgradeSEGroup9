from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django import forms

from .models import Announcement

# Create your views here.
def AnnouncementsView(request):
    num_announcements=Announcement.objects.all().count()

    return render(
        request,
        'announcement_view_all.html',
        context={
            'num_announcements':num_announcements},
    )
