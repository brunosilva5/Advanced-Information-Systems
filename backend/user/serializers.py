"""
Contains user related serializers
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from simple_email.email_confirmation import send_confirmation_email

from swot_analysis.serializers import SWOTAnalysisSerializer
from .models import User


class GetTokenSerializer(TokenObtainPairSerializer):
    """
    Override TokenObtainPairSerializer to change the messages
    """

    default_error_messages = {
        "no_active_account": _(
            "The email or password you entered is incorrect.",
        )
    }


class UserSerializer(serializers.ModelSerializer):

    """
    User model serializer
    """

    # User SWOT Analyses (nested serialization)
    analyses = SWOTAnalysisSerializer(many=True, read_only=True)

    # Additional field
    confirm_password = serializers.CharField(
        allow_blank=False,
        write_only=True,
        error_messages={
            "required": _("This is a required field."),
        },
    )

    def create(self, validated_data):
        # Get password
        password = validated_data.pop("password")
        # Get confirm password
        confirm_password = validated_data.pop("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": _("Passwords do not match.")}
            )

        # Create user object
        user = User(**validated_data)
        # Check if valid password
        try:
            validate_password(password, user=user)
        except ValidationError as exc:
            raise serializers.ValidationError({"password": exc.messages})
        # Set password
        user.set_password(password)
        # send confirmation email
        send_confirmation_email(user)

        return user

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
            "analyses",
        ]
        extra_kwargs = {
            # Define required custom messages
            "password": {
                "write_only": True,
                "error_messages": {
                    "required": _("Password is a required field."),
                },
            },
            "first_name": {
                "error_messages": {
                    "required": _("First name is a required field."),
                },
            },
            "last_name": {
                "error_messages": {
                    "required": _("Last name is a required field."),
                },
            },
        }
