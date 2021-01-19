from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.message import EmailMultiAlternatives


def send_email(
    recipient,
    subject,
    body_text,
    user_email,
    user_password,
    host,
    port,
    use_tls,
    fail_silently=False,
    body_html=None,
):
    # Create custom backend
    backend = EmailBackend(
        host=host,
        port=port,
        username=user_email,
        password=user_password,
        use_tls=use_tls,
        fail_silently=fail_silently,
    )

    # Create email object
    email = EmailMultiAlternatives(
        subject,  # email subject
        body_text,  # the body txt
        user_email,  # send from
        [recipient],  # the recipient
        connection=backend,  # use the custom backend
    )
    if body_html:
        # Attach html body
        email.attach_alternative(body_html, "text/html")
    # Send the email
    email.send()