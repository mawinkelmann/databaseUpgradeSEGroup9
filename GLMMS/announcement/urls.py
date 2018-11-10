from django.urls import path

from . import views

app_name = 'announcement'
urlpatterns = [
    path('announcement/', views.AnnouncementsView, name='view_announcements'),
]
