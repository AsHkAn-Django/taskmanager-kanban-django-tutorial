from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = '12345678'
        user = User.objects.create_user(email=email, password=password, full_name='User Userian')

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.full_name, 'User Userian')

    def test_new_user_email_normalized(self):
        email = 'test@EXAMPLE.COM'
        user = User.objects.create_user(email, 'test123', full_name='new user')
        self.assertEqual(user.email, 'test@example.com')

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'test123', full_name='invalid email')

    def test_create_new_superuser(self):
        user = User.objects.create_superuser('admin@example.com', 'pass123', full_name='admin user')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class JWTAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testjwt@example.com', password='jwtpass123', full_name='new jwt user')

    def test_jwt_token_obtain(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'email': 'testjwt@example.com', 'password': 'jwtpass123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_jwt_token_invalid_credentials(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'email': 'testjwt@example.com', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_duplicate_email_error(self):
        User.objects.create_user(email='dup@example.com', password='test123', full_name='User1')
        with self.assertRaises(Exception):
            User.objects.create_user(email='dup@example.com', password='test123', full_name='User2')