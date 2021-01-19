from django.contrib.auth.tokens import default_token_generator
from django.utils.module_loading import import_string
from django.template.loader import render_to_string
from django.urls import reverse

from hashids import Hashids

from ..mail import send_email
from .settings import settings
from django.conf import settings as django_settings

email_backend = import_string(settings.DEFAULT_BACKEND)
# Get the email field
active_field = settings.CONFIRMED_EMAIL_FIELD


def send_confirmation_email(user):

    # Check if user has 'active_field'
    if not hasattr(user, active_field):
        raise AttributeError(
            f"Class {user.__class__.__name__} has no field '{active_field}'. Please check your settings."
        )

    if not hasattr(user, "email"):
        raise AttributeError(f"Class {user.__class__.__name__} has no field 'email'.")

    # Set 'active_field' to False
    setattr(user, active_field, False)
    # Save changes
    user.save()

    # Stop here if DEBUG, and user selected it
    if not settings.SEND_IN_DEBUG and django_settings.DEBUG:
        return
    # Generate token for user
    user_token = default_token_generator.make_token(user)
    # Has user id
    hashed_user_id = Hashids(
        salt=settings.HASH_ID_SALT, min_length=settings.HASH_ID_MIN_LENGTH
    ).encode(user.id)

    # Build full url with reverse link for veryfing token
    link = settings.WEBSITE_DOMAIN + reverse(
        "verify_email_token",
        kwargs={"hashed_user_id": hashed_user_id, "token": user_token},
    )

    # Create context
    context = {"link": link, "user": user}

    # Create html body
    html_body = render_to_string(settings.EMAIL_BODY_HTML, context)

    # Create text body
    text_body = render_to_string(settings.EMAIL_BODY_TEXT, context)

    send_email(
        user.email,
        settings.EMAIL_SUBJECT,
        text_body,
        settings.USER_EMAIL_ADDRESS,
        settings.USER_EMAIL_PASSWORD,
        settings.EMAIL_HOST,
        settings.EMAIL_HOST_PORT,
        settings.USE_TLS,
        settings.FAIL_SILENTLY,
        html_body,
    )
