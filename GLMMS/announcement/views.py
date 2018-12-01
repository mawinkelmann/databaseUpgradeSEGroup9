from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.mail import send_mail
from django.contrib import messages

from .models import Announcement
from .forms import AnnouncementForm
from member.models import Profile
from django.contrib.auth.models import User

# Create your views here.

@login_required
def AnnouncementsView(request):
    announcements_list = Announcement.objects.order_by('-dateAdded')
    paginator = Paginator(announcements_list, 6) # Show 5 announcements per page

    page = request.GET.get('page')
    announcements = paginator.get_page(page)
    return render(request, 'announcement/announcement_view_all.html', {'announcements': announcements})

@login_required
def announcement_detail(request, pk):

    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'announcement/announcement_detail.html', {'announcement': announcement})

@login_required
def announcement_new(request):
    #member_list = Profile.objects.filter(member_status="A")
    #print(member_list)

    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.creator = request.user
            sender = announcement.creator.email
            announcement.save()
            if announcement.type == "H":
                subject = form.cleaned_data['title']
                message = form.cleaned_data['message']
                send_mail_from = "sender"

                recipients = []
                for profile in Profile.objects.filter(member_status="A"):
                    recipients.append(profile.phone + "@" + profile.cell_carrier_id.sms_address)
                #for user in User.objects.all():
                #    recipients.append(user.email)

                send_mail(subject, message, sender, recipients)
            return redirect('announcement:announcement_detail', pk=announcement.pk)
    else:
        form = AnnouncementForm()
    return render(request, 'announcement/announcement_edit.html', {'form': form})

@login_required
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

@login_required
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.user == announcement.creator:
        Announcement.objects.filter(pk=pk).delete()
        messages.add_message(request, messages.INFO, "Announcement Deleted.")
    else:
        messages.add_message(request, messages.INFO, "You cannot delete an announcement you did not create.")
    return redirect('announcement:AnnouncementsView')
