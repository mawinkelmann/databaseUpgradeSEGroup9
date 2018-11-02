#https://docs.djangoproject.com/en/2.1/intro/tutorial05/
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Profile
from django.contrib.auth.models import User

#test profile get values and get fields
#test profile detail view 
#test single search
#test multi search
#test edit info 

USERNAME_TEST = 'test'
PASSWORD_TEST = 'pass'
FIRST_TEST = 'first'
LAST_TEST = 'last'
BIO_TEST = 'This is a test'
created = False

def create_user(username, password, first_name, last_name):
    """
    Create a profile with the given `first_name`, last_name and email. a profile will also be created by the model
    """
    return User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)


class ProfileDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = create_user(USERNAME_TEST, PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.user.profile.bio = BIO_TEST
        cls.user.profile.member_status = Profile.ACTIVE
        cls.user.profile.pledge_class = 'Beta Omicron'
        cls.user.save()
        print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_no_profile(self):
        """
        If the user is not logged in, show them a no profile page
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('member:profile', args=(10,)))
        self.assertEqual(response.status_code, 404)
        #self.assertContains(response, "you have no profile")
        #self.assertEqual(response.context['user.profile'], False)

    def test_display_profile(self):
        """
        If the user is logged in, make sure the profile and user is being displayed
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('member:profile',args=(self.user.profile.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "{} {}".format(FIRST_TEST, LAST_TEST))
        self.assertContains(response, "{}".format(BIO_TEST))

class ProfileEditViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = create_user(USERNAME_TEST, PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.user.profile.bio = BIO_TEST
        cls.user.profile.member_status = Profile.ACTIVE
        cls.user.profile.pledge_class = 'Beta Omicron'
        cls.user.save()
        print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_no_profile_to_edit(self):
        """
        The edit profile form should not be displayed unless the user is logged in
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('member:edit_profile', args=(10,)))
        self.assertEqual(response.status_code, 404)
        #self.assertContains(response, "you have no profile")
        #self.assertEqual(response.context['user.profile'], False)

    def test_display_edit_profile(self):
        """
        A get request with should show the forms with the data prepoulated if it exists
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('member:edit_profile', args=(self.user.profile.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="first_name" value="{}"'.format(FIRST_TEST))
        self.assertContains(response, '{}'.format(BIO_TEST))

    def test_profile_edit_form(self):
        """
        A post request with invalid data should be put back on the edit_profile page with an error
        """
        from .views import ProfileEditForm
        form_data = {'birth_date': 'asdf'}
        form = ProfileEditForm(data=form_data)
        self.assertFalse(form.is_valid())

class SingleSearchViewTests(TestCase):
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
        print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_display_search(self):
        """
        The search display should show the one user as an option 
        """
        self.client.force_login(self.user)
        print(User.objects.get(pk=1).profile)
        response = self.client.get(reverse('member:single_search'))
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '{}: {} {}'.format(USERNAME_TEST, FIRST_TEST, LAST_TEST))

    def test_search(self):
        """
        The result of the post request should include the info about the requested user
        """
        print(User.objects.get(pk=1).profile)
        self.client.force_login(self.user)
        #response = self.client.get(reverse('member:single_search'))
        #print(response.content)
        response = self.client.post(reverse('member:single_search'), {'actives_choice': str(self.user.profile.id), 'inactives_choice': '', 'newmembers_choice': '', 'alumni_choice': ''}, follow=True)
        #print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, BIO_TEST)

    def test_single_search_form(self):
        print(User.objects.get(pk=1).profile)
        from .views import SingleSearchForm
        form_data = {'actives_choice': str(self.user.profile.id), 'inactives_choice': '', 'newmembers_choice': '', 'alumni_choice': ''}
        form = SingleSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
		
class MultiMemberViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = create_user(USERNAME_TEST, PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.user.profile.bio = BIO_TEST
        cls.user.profile.member_status = Profile.ACTIVE
        cls.user.profile.pledge_class = 'Beta Omicron'
        cls.user.save()
        print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_display_multi_search(self):
        """
        the page should contain the form elemetns to do a multi member search. 
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('member:multi_search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="shirt_size">shirt size')
		
    def test_multi_search_empty_groups(self):
        """
		if an empty group is searched, there should be no results.
		"""
        self.client.force_login(self.user)

        response = self.client.post(reverse('member:multi_search'), {'status_choice': "B", 'field_choice': '__all__', 'order_choice': 'pledge_class'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Results: 0')

    def test_multi_search_fields(self):
        """
		The results should contain the pledge class of the user. 
		"""
        self.client.force_login(self.user)

        response = self.client.post(reverse('member:multi_search'), {'status_choice': "__all__", 'field_choice': 'pledge_class', 'order_choice': 'pledge_class'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Beta Omicron')

        '''def test_multi_search_order_by(self):
		"""
		was_published_recently() returns True for questions whose pub_date
		is within the last day.
		"""
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)'''

class ProfileModelTests(TestCase):
    '''this class tests the methods of the Profile model'''
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = create_user(USERNAME_TEST, PASSWORD_TEST, FIRST_TEST, LAST_TEST) 
        cls.user.profile.bio = BIO_TEST
        cls.user.profile.member_status = Profile.ACTIVE
        cls.user.profile.pledge_class = 'Beta Omicron'
        cls.user.save()
        print("{} -- {}".format(cls.user.id, cls.user.profile.id))

    def test_get_printable_fields(self):
        """
        should return a list of all the fields without a certain number of them
        """
        bad_fields = ('user', 'bio', 'photo', 'jobs', 'organizations', 'positions', 'pledge_father', 'cell_carrier_id', 'id')
        fields = Profile.get_printable_fields()
        for key in fields.keys():
            self.assertNotIn(key, bad_fields)
		
    def test_get_printable_fields_and_values(self):
        """
        this should return a list of verbose names and values 
        """
        bad_fields = ('ID','user','bio', 'photo','linkedin profile','pledge father', 'cell carrier id',)
        fields = self.user.profile.get_printable_fields_and_values()
        for name, value in fields:
            self.assertNotIn(name, bad_fields)
            if name == 'member status':
                self.assertEqual(Profile.ACTIVE, value)
        