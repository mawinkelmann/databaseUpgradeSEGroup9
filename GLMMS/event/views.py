#Author: Christopher Whetsel

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.mail import send_mail, EmailMessage

from .models import Event, Event_RSVPs
from .forms import EventForm, NotificationForm

from datetime import datetime

# Create your views here.

@login_required
def events_view(request):
    '''View to handle the diaplyo f all events happening in the future '''
    today = datetime.now().date()
    events_list = Event.objects.filter(start_time__gte=today).order_by('start_time')
    paginator = Paginator(events_list, 6) # Show 5 events per page

    page = request.GET.get('page')
    events = paginator.get_page(page)
    return render(request, 'event/event_view_all.html', {'events': events, 'is_past': False})

@login_required
def past_events_view(request):
    '''View to handle the displaying of past events'''
    today = datetime.now().date()
    events_list = Event.objects.filter(start_time__lt=today).order_by('start_time')
    paginator = Paginator(events_list, 6) # Show 5 events per page

    page = request.GET.get('page')
    events = paginator.get_page(page)
    return render(request, 'event/event_view_all.html', {'events': events, 'is_past': True})

@login_required
def event_detail(request, pk):
    '''View to show the full details of an event'''
    event = get_object_or_404(Event, pk=pk)
    rsvps = Event_RSVPs.objects.filter(event=event).order_by('member__username')
    num_rsvps = rsvps.count()
    form = NotificationForm()
    return render(request, 'event/event_detail.html', {'event': event, 'num_rsvps':num_rsvps, 'rsvps': rsvps, 'form': form})

@login_required
def event_new(request):
    '''View to handle to the creation of a new event'''
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            #post.dateAdded = timezone.now()
            event.save()
            return redirect('event:event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'event/event_edit.html', {'form': form})

@login_required
def event_edit(request, pk):
    '''View to handle the editting of an event'''
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.dateAdded = timezone.now()
            event.save()
            return redirect('event:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'event/event_edit.html', {'event': event, 'form': form})

@login_required
def event_rsvp(request, pk):
    '''View that lets a user rsvp to an event once'''
    event = get_object_or_404(Event, pk=pk)
    if Event_RSVPs.objects.filter(event=event, member=request.user).count() == 0:
        Event_RSVPs.objects.create(event=event, member=request.user)
        messages.add_message(request, messages.INFO, "RSVP Successful!")
    else: 
        messages.add_message(request, messages.INFO, "You have already RSVP'ed")
    return redirect('event:event_detail', pk=pk)

@login_required
def event_delete(request, pk):
    '''View that allows the creator of an event to delete it'''
    event = get_object_or_404(Event, pk=pk)
    if request.user == event.creator:
        Event.objects.filter(pk=pk).delete()
        messages.add_message(request, messages.INFO, "Event Deleted.")
    else: 
        messages.add_message(request, messages.INFO, "You cannot delete an event you did not create.")
    return redirect('event:events_view')

@login_required
def event_notify(request, pk):
    '''View that lets the user send a message to users that have rsvped to their event'''
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        if request.user == event.creator:
            form = NotificationForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message'] + "\r\n\r\nSent by " + event.creator.first_name + " " + event.creator.last_name
                sender = "notifications@spdmizzou.org"
                reply_to = [event.creator.email]

                recipients = []
                for rsvp in Event_RSVPs.objects.filter(event=event):
                    #send an email
                    if form.cleaned_data['type'] is False:
                        recipients.append(rsvp.member.email)  
                    #send a text                          
                    elif form.cleaned_data['type'] is True:
                        recipients.append(rsvp.member.profile.phone + "@" + rsvp.member.profile.cell_carrier_id.sms_address)
                email = EmailMessage(subject, message, sender, recipients, reply_to=reply_to)
                email.send()
                #send_mail(subject, message, sender, recipients)
                messages.add_message(request, messages.INFO, "Message sent!")
        else:
            messages.add_message(request, messages.INFO, "Only the creator is allowed to send nofications.")
    return redirect('event:event_detail', pk=pk)
