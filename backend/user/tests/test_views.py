"""
Module for testing the Client API Views
"""
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
import copy
import logging

from ..models import User

logger = logging.getLogger(__name__)
logging.disable(logging.NOTSET)
logger.setLevel(logging.DEBUG)


class UserTestCase(TestCase):
    api = APIClient()

    valid_user_payload = {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john_smith42@gmail.com",
        "password": "veryCompleXpa$$word42",
        "confirm_password": "veryCompleXpa$$word42",
    }

    def create_user_and_login(self, verify_email=True) -> tuple:
        """
        Creates a user using class `valid_user_payload`, performs login,
        and returns a `tupple (access_token, refresh_token)`
        """
        # Create client
        response = self.api.post(
            reverse("create_user"),
            self.valid_user_payload,
        )
        # Assert created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(id=response.data["id"])

        self.assertFalse(
            user.is_active, "User field 'is_active' should be False on creation"  # noqa
        )

        if verify_email:
            # Set user to active (email verified)
            user.is_active = True
            user.save()

            response = self.api.post(
                reverse("login_user"),
                {
                    "email": self.valid_user_payload["email"],
                    "password": self.valid_user_payload["password"],
                },
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(
                "access",
                response.data,
                msg="Missing acess token in login response",
            )
            self.assertIn(
                "refresh",
                response.data,
                msg="Missing refresh token in login response",
            )
            return (response.data["access"], response.data["refresh"])
        else:
            response = self.api.post(
                reverse("login_user"),
                {
                    "email": self.valid_user_payload["email"],
                    "password": self.valid_user_payload["password"],
                },
            )

            # Assert that user cant login if it doesnt confirm email
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )

    def test_create_user_no_password(self):
        """
        Tests the creation of a user (POST) without password
        """
        # Create client
        no_confirm_password_payload = copy.deepcopy(self.valid_user_payload)
        del no_confirm_password_payload["confirm_password"]
        request = self.api.post(
            reverse("create_user"),
            no_confirm_password_payload,
        )

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(request.data["confirm_password"][0].code, "required")

    def test_user_login(self):
        """
        Tests the creation, login, acessing protected endpoints, logout
        """

        # Create client, and login
        access_token, refresh_token = self.create_user_and_login()

        # Test invalid token
        self.api.credentials(HTTP_AUTHORIZATION="Bearer " + "abc")
        response = self.api.get(reverse("detail_user"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test valid token
        self.api.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = self.api.get(reverse("detail_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_info(self):
        """
        Tests updating user information
        """
        # Create client
        access_token, _ = self.create_user_and_login()
        # Set authentication
        self.api.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        # Update info
        response = self.api.patch(
            reverse("detail_user"),
            {
                "first_name": "Lucas",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=response.data["id"])
        self.assertEqual(user.first_name, "Lucas")

    def test_delete_user(self):
        # Create client
        access_token, _ = self.create_user_and_login()
        # Set authentication
        self.api.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        # Delete cliente
        response = self.api.delete(reverse("detail_user"))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_login_with_unverified_email(self):
        """ Test that user can't login without veryfing email"""
        self.create_user_and_login(verify_email=False)

    def tearDown(self) -> None:
        self.api.credentials()