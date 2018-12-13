#https://docs.djangoproject.com/en/2.1/intro/tutorial05/
#Author: Christopher Whetsel

import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from datetime import datetime, date, timedelta

from .models import Event
from member.models import Profile
from django.contrib.auth.models import User

#test Event past and future 
#test Event detail 
#test Event edit 
#test rsvp
#test delete 
#test notify 
#test new

USERNAME_TEST = 'test'
PASSWORD_TEST = 'pass'
FIRST_TEST = 'first'
LAST_TEST = 'last'
BIO_TEST = 'This is a test'

EVENT_TITLE = "Demo 2 is Thrusday!"


def create_user(username, password, first_name, last_name):
    """
    Create a profile with the given `first_name`, last_name and email. a profile will also be created by the model
    """
    return User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)


def create_event(user, title, topic, pub, start_time):
    return Event.objects.create(
        creator = user,
        title = title,
        topic = topic,
        is_public = pub,
        description = "DESCRIPTION", 
        address = "ADDRESS",
        city = "CITY",
        state = "STATE", 
        zipcode = "ZIPCODE", 
        start_time = start_time,
        end_time = datetime.now()
    )

class EventDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = create_user(USERNAME_TEST, PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.user.profile.bio = BIO_TEST
        cls.user.profile.member_status = Profile.ACTIVE
        cls.user.profile.pledge_class = 'Beta Omicron'
        cls.user.save()

        cls.other_user = create_user("other", PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.other_user.profile.bio = BIO_TEST
        cls.other_user.profile.member_status = Profile.ACTIVE
        cls.other_user.profile.pledge_class = 'Beta Omicron'
        cls.other_user.save()

        start = datetime.now()
        cls.event = create_event(cls.user, EVENT_TITLE, 'A', True, start)
        #print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_no_event(self):
        """
        If the event does not exist
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('event:event_detail', args=(10,)))
        self.assertEqual(response.status_code, 404)

    def test_detail(self):
        """
        If the user is not logged in, show them a no profile page
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('event:event_detail', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, EVENT_TITLE)
        self.assertContains(response, "Notify RSVPs")

    def test_detail_not_creator(self):
        """
        If the user is logged in, make sure the profile and user is being displayed
        """
        self.client.force_login(self.other_user)

        response = self.client.get(reverse('event:event_detail', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, EVENT_TITLE)
        self.assertNotContains(response, "Notify RSVPs")

class EventEditViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = create_user(USERNAME_TEST, PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.user.profile.bio = BIO_TEST
        cls.user.profile.member_status = Profile.ACTIVE
        cls.user.profile.pledge_class = 'Beta Omicron'
        cls.user.save()

        cls.other_user = create_user("other", PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.other_user.profile.bio = BIO_TEST
        cls.other_user.profile.member_status = Profile.ACTIVE
        cls.other_user.profile.pledge_class = 'Beta Omicron'
        cls.other_user.save()

        start = datetime.now()
        cls.event = create_event(cls.user, EVENT_TITLE, 'A', True, start)
        #print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_no_event_to_edit(self):
        """
        The edit form only shows for 
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('event:event_edit', args=(10,)))
        self.assertEqual(response.status_code, 404)

    def test_display_edit_event(self):
        """
        A get request with should show the forms with the data prepoulated if it exists
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('event:event_edit', args=(self.event.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, EVENT_TITLE)
        self.assertContains(response, "DESCRIPTION")

    def test_event_edit_form(self):
        """
        A post request with invalid data should be put back on the edit_profile page with an error
        """
        from .forms import EventForm
        form_data = {'title': 'this is a title'}
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
        #form = EventForm(instance=self.event)
        #self.assertTrue(form.is_valid())

class EventViewTests(TestCase):
    '''Tests for the views and forms used in the single searching feature.'''
    #NOTE: these fail. not sure why yet, but the user is not populated into the selects as an option for some reason by the Form
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = create_user(USERNAME_TEST, PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.user.profile.bio = BIO_TEST
        cls.user.profile.member_status = Profile.ACTIVE
        cls.user.profile.pledge_class = 'Beta Omicron'
        cls.user.save()

        cls.other_user = create_user("other", PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.other_user.profile.bio = BIO_TEST
        cls.other_user.profile.member_status = Profile.ACTIVE
        cls.other_user.profile.pledge_class = 'Beta Omicron'
        cls.other_user.save()

        start = datetime.now()
        cls.event = create_event(cls.user, EVENT_TITLE, 'A', True, start)
        #print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_view_future(self):
        """
        The result of the post request should include the info about the requested user
        """
        self.client.force_login(self.user)
        another_title = "This is another title."
        create_event(self.user, another_title, 'B', False, datetime.now())

        response = self.client.get(reverse('event:events_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, EVENT_TITLE)
        self.assertContains(response, "Social Event")
    
    def test_view_past(self):
        """
        The result of the post request should include the info about the requested user
        """
        self.client.force_login(self.user)
        another_title = "This is another title."
        create_event(self.user, another_title, 'B', False, date.today() - timedelta(1))

        response = self.client.get(reverse('event:past_events'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, EVENT_TITLE)
        self.assertContains(response, another_title)
		
class EventRSVPTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = create_user(USERNAME_TEST, PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.user.profile.bio = BIO_TEST
        cls.user.profile.member_status = Profile.ACTIVE
        cls.user.profile.pledge_class = 'Beta Omicron'
        cls.user.save()

        cls.other_user = create_user("other", PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.other_user.profile.bio = BIO_TEST
        cls.other_user.profile.member_status = Profile.ACTIVE
        cls.other_user.profile.pledge_class = 'Beta Omicron'
        cls.other_user.save()

        start = datetime.now()
        cls.event = create_event(cls.user, EVENT_TITLE, 'A', True, start)
        #print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_rsvp(self):
        """
        the page should contain the form elemetns to do a multi member search. 
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('event:event_rsvp', args=(self.event.id,)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RSVP Successful!")
        response = self.client.get(reverse('event:event_rsvp', args=(self.event.id,)), follow=True)
        self.assertContains(response, "You have already RSVP")
	
class EventDeleteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = create_user(USERNAME_TEST, PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.user.profile.bio = BIO_TEST
        cls.user.profile.member_status = Profile.ACTIVE
        cls.user.profile.pledge_class = 'Beta Omicron'
        cls.user.save()

        cls.other_user = create_user("other", PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.other_user.profile.bio = BIO_TEST
        cls.other_user.profile.member_status = Profile.ACTIVE
        cls.other_user.profile.pledge_class = 'Beta Omicron'
        cls.other_user.save()

        start = datetime.now()
        cls.event = create_event(cls.user, EVENT_TITLE, 'A', True, start)
        #print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_delete(self):
        """
        the page should contain the form elemetns to do a multi member search. 
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('event:event_delete', args=(self.event.id,)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Event Deleted.")

class EventNotifyTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = create_user(USERNAME_TEST, PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.user.profile.bio = BIO_TEST
        cls.user.profile.member_status = Profile.ACTIVE
        cls.user.profile.pledge_class = 'Beta Omicron'
        cls.user.save()

        cls.other_user = create_user("other", PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.other_user.profile.bio = BIO_TEST
        cls.other_user.profile.member_status = Profile.ACTIVE
        cls.other_user.profile.pledge_class = 'Beta Omicron'
        cls.other_user.save()

        start = datetime.now()
        cls.event = create_event(cls.user, EVENT_TITLE, 'A', True, start)
        #print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_notify(self):
        """
        the page should contain the form elemetns to do a multi member search. 
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse('event:event_notify', args=(self.event.id,)), {'subject': 'Test', 'message': 'test message'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Message sent!")
