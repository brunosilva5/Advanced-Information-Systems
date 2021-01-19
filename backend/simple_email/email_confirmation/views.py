from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from hashids import Hashids
from django.contrib.auth import get_user_model
from .settings import settings


def verify(request, hashed_user_id, token):

    # Unhash the user id
    user_id = Hashids(
        salt=settings.HASH_ID_SALT, min_length=settings.HASH_ID_MIN_LENGTH
    ).decode(hashed_user_id)[0]

    # Get user id
    user = get_user_model().objects.get(id=user_id)

    # Check if token is valid
    is_token_valid = default_token_generator.check_token(user, token)
    if is_token_valid:
        # Get active field
        active_field = settings.CONFIRMED_EMAIL_FIELD
        # Set user to active
        setattr(user, active_field, True)
        # Set last login
        user.last_login = timezone.now()
        # Save the user
        user.save()

    # Get template
    template = settings.CONFIRM_PAGE

    return render(request, template, {"success": is_token_valid})
