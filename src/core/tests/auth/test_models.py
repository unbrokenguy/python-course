import pytest
from django.utils.crypto import get_random_string

from authentication.models import User, send_email


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
    send_email(
        subject="Confirm Email",
        to_email=email,
        template="authentication/mail.html",
        args=dict(code=get_random_string(), name=get_random_string()),
    )
