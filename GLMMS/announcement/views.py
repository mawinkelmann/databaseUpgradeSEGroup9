from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django import forms

from .models import Announcement

# Create your views here.

def AnnouncementsView(request):

    template_name = 'member/profile.html'

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'announcement_view_all.html',
        context={
            'num_visits':num_visits},
    )
