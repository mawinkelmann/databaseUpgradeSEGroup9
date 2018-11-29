from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Event
from .forms import EventForm

# Create your views here.

@login_required
def EventsView(request):
    events_list = Event.objects.order_by('start_time')
    paginator = Paginator(events_list, 6) # Show 5 events per page

    page = request.GET.get('page')
    events = paginator.get_page(page)
    return render(request, 'event/event_view_all.html', {'events': events})

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event/event_detail.html', {'event': event})

@login_required
def event_new(request):
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
    return render(request, 'event/event_edit.html', {'form': form})

@login_required
def event_rsvp(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        Event_RSVPs.objects.create(event=event, user=request.user)
        message = "RSVP successful"
        return redirect('event:event_detail', pk=pk, context={'message':message})
    return redirect('event:event_detail', pk=pk)
