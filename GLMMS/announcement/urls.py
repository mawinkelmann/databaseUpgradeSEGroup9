from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'announcement'
urlpatterns = [
    path('announcement', views.AnnouncementsView, name='AnnouncementsView'),
    path('announcement/search/', views.AnnouncementsViewSearch, name='AnnouncementsViewSearch'),
    path('announcement/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('announcement/new', views.announcement_new, name='announcement_new'),
    path('announcement/<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('announcement/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
    url(r'^search/$', views.search, name='search'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_announcement, name='add_comment_to_announcement'),
]
