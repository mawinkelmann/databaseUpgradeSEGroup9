from django.test import TestCase

# Create your tests here.
#https://docs.djangoproject.com/en/2.1/intro/tutorial05/
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from datetime import datetime, date, timedelta

from .models import Announcement
from member.models import Profile
from django.contrib.auth.models import User

#test Announcement past and future 
#test Announcement detail 
#test Announcement edit 
#test rsvp
#test delete 
#test notify 
#test new

USERNAME_TEST = 'test'
PASSWORD_TEST = 'pass'
FIRST_TEST = 'first'
LAST_TEST = 'last'
BIO_TEST = 'This is a test'

ANNOUNCEMENT_TITLE = "Demo 2 is Thrusday!"


def create_user(username, password, first_name, last_name):
    """
    Create a profile with the given `first_name`, last_name and email. a profile will also be created by the model
    """
    return User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)


def create_announcement(user, title, topic):
    return Announcement.objects.create(
        creator = user,
        title = title,
        topic = topic,
        type = 'G',
        message = "MESSAGE"
    )

class AnnouncementDetailViewTests(TestCase):
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
        cls.announcement = create_announcement(cls.user, ANNOUNCEMENT_TITLE, 'A')
        #print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_no_announcement(self):
        """
        If the announcement does not exist
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('announcement:announcement_detail', args=(10,)))
        self.assertEqual(response.status_code, 404)

    def test_detail(self):
        """
        If the user is not logged in, show them a no profile page
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('announcement:announcement_detail', args=(self.announcement.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ANNOUNCEMENT_TITLE)
        self.assertContains(response, "Edit")

    def test_detail_not_creator(self):
        """
        If the user is logged in, make sure the profile and user is being displayed
        """
        self.client.force_login(self.other_user)

        response = self.client.get(reverse('announcement:announcement_detail', args=(self.announcement.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ANNOUNCEMENT_TITLE)
        self.assertNotContains(response, "Notify RSVPs")

class AnnouncementEditViewTests(TestCase):
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
        cls.announcement = create_announcement(cls.user, ANNOUNCEMENT_TITLE, 'A')
        #print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_no_announcement_to_edit(self):
        """
        The edit form only shows for 
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('announcement:announcement_edit', args=(10,)))
        self.assertEqual(response.status_code, 404)

    def test_display_edit_announcement(self):
        """
        A get request with should show the forms with the data prepoulated if it exists
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('announcement:announcement_edit', args=(self.announcement.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ANNOUNCEMENT_TITLE)
        self.assertContains(response, "MESSAGE")

    def test_announcement_edit_form(self):
        """
        A post request with invalid data should be put back on the edit_profile page with an error
        """
        from .forms import AnnouncementForm
        form_data = {'title': 'this is a title'}
        form = AnnouncementForm(data=form_data)
        self.assertFalse(form.is_valid())
        #form = AnnouncementForm(instance=self.announcement)
        #self.assertTrue(form.is_valid())

class AnnouncementViewTests(TestCase):
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
        cls.announcement = create_announcement(cls.user, ANNOUNCEMENT_TITLE, 'A')
        #print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_announcement_view(self):
        """
        The result of the post request should include the info about the requested user
        """
        self.client.force_login(self.user)
        another_title = "This is another title."
        create_announcement(self.user, another_title, 'B')

        response = self.client.get(reverse('announcement:AnnouncementsView'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ANNOUNCEMENT_TITLE)
        self.assertContains(response, self.announcement.creator)

class AnnouncementDeleteTests(TestCase):
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
        cls.announcement = create_announcement(cls.user, ANNOUNCEMENT_TITLE, 'A')
        #print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_delete(self):
        """
        the page should contain the form elemetns to do a multi member search. 
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('announcement:announcement_delete', args=(self.announcement.id,)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Announcement Deleted.")