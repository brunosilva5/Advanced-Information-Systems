"""
Module for testing the User and Client models
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import User


class UserTestCase(TestCase):
    unique_email = "some_random_email@gmail.com"

    def setUp(self):
        """
        Create default user
        """
        User.objects.create(
            email=self.unique_email,
            first_name="Joe",
            last_name="Gates",
        )

    def test_user_unique_email(self):
        """
        Tests the creation of a user with a repeated email.
        Should raise exception
        """
        with self.assertRaises(ValidationError) as exc:
            user = User(email=self.unique_email)
            user.full_clean()

        exception = exc.exception
        self.assertIn("email", exception.error_dict)
        email_exceptions = exception.error_dict["email"]
        self.assertEqual(1, len(email_exceptions))
        email_exception = email_exceptions[0]
        self.assertEqual("unique", email_exception.code)

    def test_user_invalid_email(self):
        """
        Tests the creation of a user with a invalid email.
        Should raise exception
        """
        with self.assertRaises(ValidationError) as exc:
            user = User(email="not_a_valid_email")
            user.full_clean()

        exception = exc.exception
        self.assertIn("email", exception.error_dict)
        email_exceptions = exception.error_dict["email"]
        self.assertEqual(1, len(email_exceptions))
        email_exception = email_exceptions[0]
        self.assertEqual("invalid", email_exception.code)

    def test_required_user_fields(self):
        """
        Tests the creation of a user without required fields
        Should raise exception.
        """
        with self.assertRaises(ValidationError) as exc:
            user = User()
            user.full_clean()

        exception = exc.exception
        for field in ["password", "email", "first_name", "last_name"]:
            self.assertIn(field, exception.error_dict)
            field_exceptions = exception.error_dict[field]
            self.assertEqual(1, len(field_exceptions))
            field_exception = field_exceptions[0]
            self.assertEqual("blank", field_exception.code)
