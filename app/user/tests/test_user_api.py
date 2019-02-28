from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token_obtain_pair')
PROFILE_URL = reverse('user:profile')


def create_user(**params):
    return User.objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_successful(self):
        """Test creating user with valid payload successfully"""
        payload = {
            'email': 'test@test.net',
            'password': 'password1234',
            # Following payload fields are optional
            'first_name': 'User',
            'last_name': 'Test',
            'username': 'userTest',
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {
            'email': 'test@test.net',
            'password': 'test1234'
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 8 characters"""
        payload = {'email': 'test@test.net', 'password': '1234567'}
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = User.objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'test@test.net',
            'password': 'test1234'
        }
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)
        self.assertIn('access', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials_failure(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@test.net', password='test1234')
        payload = {
            'email': 'test@test.net',
            'password': 'test1243'
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('access', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_no_user_failure(self):
        """Test that token is not created if user doesn't exist"""
        payload = {
            'email': 'test@test.net',
            'password': 'test1234'
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('access', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token__missing_field_failure(self):
        """Test that email and password are required"""
        response = self.client.post(TOKEN_URL, {'email': 'test@test.net',
                                                'password': ''})
        self.assertNotIn('access', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_details_unauthorized_failure(self):
        """Test that authentication is required to see own details"""
        response = self.client.get(PROFILE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@test.net',
            password='test1234',
            username='testUser',
            first_name='Test',
            last_name='User'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_successful(self):
        """Test retrieving the profile for a logged user"""
        response = self.client.get(PROFILE_URL)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'username': self.user.username,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that post is not allowed in the me url"""
        response = self.client.post(PROFILE_URL, {})
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'first_name': 'New Name', 'password': 'password123'}
        response = self.client.patch(PROFILE_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
