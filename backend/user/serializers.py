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


from .models import User


class GetTokenSerializer(TokenObtainPairSerializer):
    """
    Override TokenObtainPairSerializer to change the messages
    """

    default_error_messages = {
        "no_active_account": _("O email ou a palavra-passe está incorrecto.")
    }


class UserSerializer(serializers.ModelSerializer):

    """
    User model serializer
    """

    # Additional field
    confirm_password = serializers.CharField(
        allow_blank=False,
        write_only=True,
        error_messages={
            "required": _(
                "O confirmar palavra-passe é um campo de preenchimento obrigatório."
            ),
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
                {"password": _("As palavras-passes não coincidem!")}
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
        ]
        extra_kwargs = {
            # Define required custom messages
            "password": {
                "write_only": True,
                "error_messages": {
                    "required": _(
                        "A palavra-passe é um campo de preenchimento obrigatório."
                    )
                },
            },
            "first_name": {
                "error_messages": {
                    "required": _(
                        "O primeiro nome é um campo de preenchimento obrigatório."
                    )
                },
            },
            "last_name": {
                "error_messages": {
                    "required": _(
                        "O último nome é um campo de preenchimento obrigatório."
                    )
                },
            },
        }
