from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    User model manager where email is the unique identifier
    for authentication, instead of username.
    """

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a User with the given email and password
        """
        if not email:
            raise ValueError(_("Email é um campo de preenchimento obrigatório."))

        if not first_name:
            raise ValueError(_("Primeiro nome é um campo de preenchimento obrigatório"))

        if not last_name:
            raise ValueError(_("Último nome é um campo de preenchimento obrigatório"))

        # Normalize email
        email = self.normalize_email(email)

        # Create user instance
        user = self.model(email=email, **extra_fields)

        # Set user password (hashing)
        user.set_password(password)

        # Save user
        user.save()

        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, first_name, last_name, password, **extra_fields)