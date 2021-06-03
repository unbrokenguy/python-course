import pytest
from django.urls import reverse
from django.utils.crypto import get_random_string

from authentication.models import User
from core.tests.user_factory import UserFactory


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
    assert response["Location"] == reverse("root")


@pytest.mark.django_db
def test_sign_up_fail(client):
    response = client.post(
        "/auth/sign_up/",
        {
            "random_parameter1": get_random_string(),
            "random_parameter2": get_random_string(),
            "email": get_random_string() + "@example.com",
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_sign_in_fail(client):
    user, password = UserFactory.create(), get_random_string()
    response = client.post(
        "/auth/sign_in/",
        {"email": user.email, "password": password},
    )
    assert response.status_code == 400


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


@pytest.mark.django_db
def test_confirm_success(client):
    user = UserFactory.create()
    user.set_password(get_random_string())
    user.save()
    response = client.get(f"/auth/confirm/{user.confirmation_code}")
    assert response.status_code == 200
    assert "Your account confirm successful" in response.content.decode("utf-8")
    assert User.objects.get(confirmation_code=user.confirmation_code).is_confirmed == "CONFIRMED"


@pytest.mark.django_db
def test_confirm_fail(client):
    user = UserFactory.create()
    user.set_password(get_random_string())
    user.is_confirmed = "CONFIRMED"
    user.save()
    response = client.get(f"/auth/confirm/{user.confirmation_code}")
    assert response.status_code == 200
    assert "Wrong confirmation code" in response.content.decode("utf-8")
