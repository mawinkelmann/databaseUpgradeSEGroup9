from django.urls import path

from . import views

app_name = 'event'
urlpatterns = [
    path('event', views.EventsView, name='EventsView'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/new', views.event_new, name='event_new'),
    path('event/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('event/<int:pk>/rsvp/', views.event_rsvp, name='event_rsvp'),
]