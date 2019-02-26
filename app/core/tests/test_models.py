from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with email as username successfully"""
        email = 'test@test.net'
        password = 'test1234'
        user = User.objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
