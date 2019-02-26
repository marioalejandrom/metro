from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with
        email as username successfully"""
        email = 'test@test.net'
        password = 'test1234'
        user = User.objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_invalid_email_failure(self):
        """Test creating an user with invalid email raises error"""
        email = 'test@googlecom'  # or empty
        password = 'test1234'
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email=email,
                password=password
            )

    def test_new_user_email_normalized(self):
        """Test that the email for new user is normalized"""
        email = 'test@TEST.net'
        user = User.objects.create_user(
            email=email,
            password='1234Password'
        )
        self.assertEqual(user.email, email.lower())

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = User.objects.create_superuser(
            email='test@test.net',
            password='test1234'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
