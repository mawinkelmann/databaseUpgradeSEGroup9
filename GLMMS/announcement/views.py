from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpRequest, Http404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django import forms

from .models import Announcement

# Create your views here.

class AnnouncementsView(generic.ListView):
    model = Announcement
    template_name = 'announcement_view_all.html'

    #order_by = request.GET.get('order_by', 'defaultOrderField')
    #Model.objects.all().order_by(order_by)

    def get_queryset(self):
        return Announcement.objects.all()
