from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django import forms

from .models import Announcement
from .forms import AnnouncementForm

# Create your views here.


def AnnouncementsView(request):

    announcements = Announcement.objects.order_by('-dateAdded')
    return render(request, 'announcement/announcement_view_all.html', {'announcements': announcements})

def announcement_detail(request, pk):

    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'announcement/announcement_detail.html', {'announcement': announcement})

def announcement_new(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.creator = request.user
            #post.dateAdded = timezone.now()
            announcement.save()
            return redirect('announcement:announcement_detail', pk=announcement.pk)
    else:
        form = AnnouncementForm()
    return render(request, 'announcement/announcement_edit.html', {'form': form})

def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.creator = request.user
            announcement.dateAdded = timezone.now()
            announcement.save()
            return redirect('announcement:announcement_detail', pk=announcement.pk)
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'announcement/announcement_edit.html', {'form': form})
