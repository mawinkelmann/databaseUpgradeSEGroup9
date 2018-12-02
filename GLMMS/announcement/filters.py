import django_filters

from announcement.models import Announcement

class AnnouncementFilter(django_filters.FilterSet):
    creator = django_filters.CharFilter(lookup_expr='username__icontains')
    type = django_filters.ChoiceFilter(choices=Announcement.TYPES)
    topic = django_filters.ChoiceFilter(choices=Announcement.TOPICS)
    class Meta:
        model = Announcement
        fields = ['creator', 'type', 'topic']
