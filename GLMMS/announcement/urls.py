from django.urls import path

from . import views

app_name = 'announcement'
urlpatterns = [
    path('announcement', views.AnnouncementsView, name='AnnouncementsView'),
    path('announcement/<int:pk>/', views.announcement_detail, name='announcement_detail'),
]
