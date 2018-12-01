from django.urls import path

from . import views

app_name = 'announcement'
urlpatterns = [
    path('announcement', views.AnnouncementsView, name='AnnouncementsView'),
    path('announcement/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('announcement/new', views.announcement_new, name='announcement_new'),
    path('announcement/<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('announcement/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
]
