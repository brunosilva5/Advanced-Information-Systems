from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager


class User(AbstractUser):
    # Disable username field
    username = None

    # Email Field
    email = models.EmailField(
        _("Endereço email"),
        unique=True,
        error_messages={
            "unique": _("Este email já se encontra associado a uma conta existente."),
        },
    )

    # First name field
    first_name = models.CharField(
        _("Primeiro nome"), max_length=100, blank=False, null=False
    )

    # Last name field
    last_name = models.CharField(
        _("Último nome"), max_length=100, null=False, blank=False
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
        verbose_name = _("Utilizador")
        verbose_name_plural = _("Utilizadores")
