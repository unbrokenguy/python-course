import pytest
from core.tests.testconf import client
from django.urls import reverse
from django.utils.crypto import get_random_string

from core.tests.user_factory import UserFactory

bad_passwords = [
    "12345",
    "987654321",
    "qwertyuiop",
    "same_as_email",
]

@pytest.mark.django_db
@pytest.mark.parametrize("password", bad_passwords)
def test_sign_up_fail(client, password):
    email = get_random_string() + "@gmail.com"
    response = client.post(
        "/auth/sign_up/",
        {
            "first_name": get_random_string(),
            "last_name": get_random_string(),
            "email": email,
            "password": email if password == "same_as_email" else password,
            "confirm_password": email if password == "same_as_email" else password,
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_sign_up_success(client):
    password = get_random_string()
    response = client.post(
        "/auth/sign_up/",
        {
            "first_name": get_random_string(),
            "last_name": get_random_string(),
            "email": get_random_string() + "@example.com",
            "password": password,
            "confirm_password": password,
        },
    )
    assert response.status_code == 302
    assert response['Location'] == reverse('root')


@pytest.mark.django_db
def test_sign_in_fail(client):
    user, password = UserFactory.create(), get_random_string()
    response = client.post(
        "/auth/sign_in/",
        {"email": user.email, "password": password},
    )
    assert response.status_code == 200
    assert "Incorrect login or password or you need to confirm your account" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_sign_out_success(client):
    user = UserFactory.create()
    password = get_random_string()
    user.set_password(password)
    user.is_confirmed = "CONFIRMED"
    user.save()
    client.force_login(user)
    response = client.get("/auth/sign_out/")
    assert response.status_code == 302
