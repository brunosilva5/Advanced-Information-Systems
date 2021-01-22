from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager


class User(AbstractUser):
    # Disable username field
    username = None

    # Email Field
    email = models.EmailField(
        _("Email address"),
        unique=True,
        error_messages={
            "unique": _("This email is already associated with an existing account."),
        },
    )

    # First name field
    first_name = models.CharField(
        _("First name"), max_length=100, blank=False, null=False
    )

    # Last name field
    last_name = models.CharField(
        _("Last name"), max_length=100, null=False, blank=False
    )

    # Use the custom manager
    objects = UserManager()

    # Define email as primary field
    USERNAME_FIELD = "email"

    # Define mandatory fields
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    # String representation of User model
    def __str__(self):
        # Defined in Abstract User
        return self.get_full_name()

    class Meta:  # noqa
        verbose_name = _("User")
        verbose_name_plural = _("Users")
