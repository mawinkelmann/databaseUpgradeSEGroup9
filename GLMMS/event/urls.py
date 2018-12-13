#Author: Christopher Whetsel

from django.urls import path

from . import views

app_name = 'event'
urlpatterns = [
    path('', views.events_view, name='events_view'),
    path('event/past/', views.past_events_view, name="past_events"),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/new/', views.event_new, name='event_new'),
    path('event/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('event/<int:pk>/rsvp/', views.event_rsvp, name='event_rsvp'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('event/<int:pk>/notify/', views.event_notify, name='event_notify'),
]