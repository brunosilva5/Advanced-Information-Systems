from ..errors import MissingSetting
from django.conf import settings as django_settings
from simple_email.settings import settings

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def parse_email_confirmation_settings(global_settings: dict):

    required_nested_settings = [
        "USER_EMAIL_ADDRESS",
        "USER_EMAIL_PASSWORD",
        "WEBSITE_DOMAIN",
    ]
    if "EMAIL_CONFIRMATION" not in global_settings:
        raise MissingSetting(
            "Missing setting 'VERIFICATION_EMAIL' for SIMPLE_MAIL. Please check your settings."
        )

    verification_email_settings = global_settings.pop("EMAIL_CONFIRMATION")

    for setting in required_nested_settings:
        if setting not in verification_email_settings:
            raise AttributeError(
                f"Missing setting '{setting}' in 'EMAIL_CONFIRMATION'. Check your settings."
            )

    return_settings = {}

    return_settings["USER_EMAIL_ADDRESS"] = verification_email_settings[
        "USER_EMAIL_ADDRESS"
    ]
    return_settings["USER_EMAIL_PASSWORD"] = verification_email_settings[
        "USER_EMAIL_PASSWORD"
    ]
    return_settings["WEBSITE_DOMAIN"] = verification_email_settings["WEBSITE_DOMAIN"]

    return_settings["DEFAULT_BACKEND"] = verification_email_settings.get(
        "DEFAULT_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
    )

    return_settings["SEND_IN_DEBUG"] = verification_email_settings.get(
        "SEND_IN_DEBUG", False
    )

    return_settings["CONFIRMED_EMAIL_FIELD"] = verification_email_settings.get(
        "CONFIRMED_EMAIL_FIELD", "is_active"
    )

    return_settings["EMAIL_SUBJECT"] = verification_email_settings.get(
        "EMAIL_SUBJECT", "Confirm your account"
    )

    return_settings["EMAIL_BODY_HTML"] = verification_email_settings.get(
        "EMAIL_BODY_HTML", "body_html.html"
    )

    return_settings["EMAIL_BODY_TEXT"] = verification_email_settings.get(
        "EMAIL_BODY_TEXT", "body_text.txt"
    )

    return_settings["CONFIRM_PAGE"] = verification_email_settings.get(
        "simple_email/confirm_page.html", "confirm_page.html"
    )

    return_settings["FAIL_SILENTLY"] = verification_email_settings.get(
        "FAIL_SILENTLY", False
    )
    return_settings["USE_TLS"] = verification_email_settings.get("USE_TLS", True)

    return_settings["HASH_ID_MIN_LENGTH"] = verification_email_settings.get(
        "HASH_ID_MIN_LENGTH", 20
    )

    return_settings["HASH_ID_SALT"] = verification_email_settings.get(
        "HASH_ID_SALT", django_settings.SECRET_KEY
    )
    return_settings["EMAIL_HOST"] = verification_email_settings.get(
        "EMAIL_HOST", "smtp.gmail.com"
    )
    return_settings["EMAIL_HOST_PORT"] = verification_email_settings.get(
        "EMAIL_HOST_PORT", 587
    )
    # Merge both dicts
    return {**global_settings, **return_settings}


class EmailConfirmationSettings:
    def __init__(self):
        self.settings = parse_email_confirmation_settings(settings)

    def __getattr__(self, name):
        return self.settings[name]


settings = EmailConfirmationSettings()