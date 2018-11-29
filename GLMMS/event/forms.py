from django import forms
from django.contrib.auth.models import User

from .models import Event

class SplitDateTimeWidget(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some
    """
    template_name = 'admin/widgets/split_datetime.html'

    def __init__(self, attrs=None):
        widgets = [forms.widgets.DateInput(attrs={'type':'date'}), forms.widgets.TimeInput]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['date_label'] = 'Date:'
        context['time_label'] = 'Time (24-hour hh:mm:ss):'
        return context

class EventForm(forms.ModelForm):
    '''This class provides an event creation form.'''
    class Meta: 
        model = Event
        fields = ['topic', 'title', 'description', 'start_time', 'end_time', 'is_public', 'address', 'city', 'state', 'zipcode']
        field_classes = {
            'start_time': forms.SplitDateTimeField,
            'end_time': forms.SplitDateTimeField, 
        }
        widgets = {
            'start_time': SplitDateTimeWidget(),
            'end_time': SplitDateTimeWidget(),
        }
        help_texts = {
            'is_public': ('Should this event be visible outside the Fraternity?'),
        }
        labels = {
            'is_public': ('Public Event?'),
        }
