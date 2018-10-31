from django.urls import path

from . import views

app_name = 'member'
urlpatterns = [
	path('search', views.search_index, name='search_index'),
	path('search/single/', views.single_search, name='single_search'),
	path('search/multi/', views.multi_search, name='mult_search'),
	path('search/job/', views.job_search, name='job_search'),
	path('search/position/', views.position_search, name='position_search'),
	path('search/organization/', views.org_search, name='organization_search'),
	path('search/profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile'),
	path('search/profile/edit/<int:profile_id>', views.edit_info, name='edit_profile'),
]

'''urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
	path('<int:pk>/', views.SingleDetailView.as_view(), name='single_detail'),
	path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
	path('<int:question_id>/vote/', views.vote, name='vote'),
]'''