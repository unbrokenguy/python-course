import pytest
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.conf import settings
from authentication.models import User
from authentication.tasks import send_email


@pytest.mark.django_db
def test_no_username_user_manager():
    email = get_random_string() + "@example.com"
    User.objects.create_superuser(email=email, password=get_random_string())
    user = User.objects.get(email=email)
    assert user.username == user.email
    assert str(user) == email


@pytest.mark.django_db
def test_send_email_success():
    email = get_random_string() + "@example.com"
    html_message = render_to_string(
        template_name="authentication/mail.html",
        context=dict(code=get_random_string(), name=get_random_string(), server_url=settings.ALLOWED_HOSTS[0]),
    )
    send_email.delay(
        subject="Confirm Email",
        html_message=html_message,
        recipient_list=[email],
    )
