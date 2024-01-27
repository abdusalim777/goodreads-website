from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username': 'abdusalimjon',
                'first_name': 'abdusalimbe',
                'last_name': 'shoirjonov',
                'email': 'sayitqulov@gmail.com',
                'password': '1234'
            }
        )

        user = CustomUser.objects.get(username='abdusalimjon')

        self.assertEqual(user.first_name, 'abdusalimbe')
        self.assertEqual(user.last_name, 'shoirjonov')
        self.assertEqual(user.email, 'sayitqulov@gmail.com')
        self.assertNotEqual(user.password, '1234')
        self.assertTrue(user.check_password('1234'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name': 'abdusalimbe',
                'email': 'sayitqulov@gmail.com'
            }
        )

        user_count =CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'abdusalimjon',
                'first_name': 'abdusalimbe',
                'last_name': 'shoirjonov',
                'email': 'sayitqulov',
                'password': '1234'
            }
        )
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        user = CustomUser.objects.create(username='abdusalimjon', first_name='abdusalimbe')
        user.set_password('12345')
        user.save()

        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'abdusalimjon',
                'first_name': 'abdusalimbe',
                'last_name': 'shoirjonov',
                'email': 'sayitqulov',
                'password': '1234'
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class LoginTesCase(TestCase):
    def setUp(self):
        # DRY don't repeat yourself
        self.db_user = CustomUser.objects.create(username='abdusalimjon', first_name='abdusalimbe')
        self.db_user.set_password('1234')
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'abdusalimjon',
                'password': '1234',
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'abdulla',
                'password': '1234',
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'abdusalimjon',
                'password': '1234567',
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username='abdusalimjon', password='1234')

        self.client.get(reverse('users:logout'))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login') + '?next=/users/profile/')

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username='abdusalimjon',
            first_name='abdusalimbe',
            last_name='shoirjonov',
            email='sayitqulov@gmail.com'
        )
        user.set_password('12345')
        user.save()

        self.client.login(username='abdusalimjon', password='12345')

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username='abdusalimjon',
            first_name='abdusalimbe',
            last_name='shoirjonov',
            email='sayitqulov@gmail.com'
        )
        user.set_password('12345')
        user.save()

        self.client.login(username='abdusalimjon', password='12345')

        response = self.client.post(
            reverse('users:profile_edit'),
            data={
                'username': 'abdusalimjon',
                'first_name': 'abdusalimbe',
                'last_name': "sayitqulov",
                'email': 'sayitqulov1@gmail.com',
            }
        )

        user.refresh_from_db()

        self.assertEqual(user.last_name, 'sayitqulov')
        self.assertEqual(user.email, 'sayitqulov1@gmail.com')
        self.assertEqual(response.url, reverse('users:profile'))
