import pytest
from django.urls import reverse
from django.utils.crypto import get_random_string

from authentication.models import User
from core.tests.user_factory import UserFactory

bad_passwords = ["12345", "987654321", "qwertyuiop", "same_as_email", "different"]


@pytest.fixture
def user():
    user = UserFactory.create()
    user.set_password(get_random_string())
    user.is_confirmed = "CONFIRMED"
    user.save()
    return user


@pytest.mark.django_db
@pytest.mark.parametrize("password", bad_passwords)
def test_sign_up_fail(client, password):
    email = get_random_string() + "@gmail.com"
    bad_password = email if password == "same_as_email" else password
    confirm_password = (email if password == "same_as_email" else password,)
    if bad_password == "different":
        bad_password = get_random_string()
        confirm_password = bad_password[::-1]
    response = client.post(
        "/auth/sign_up/",
        {
            "first_name": get_random_string(),
            "last_name": get_random_string(),
            "email": email,
            "password": bad_password,
            "confirm_password": confirm_password,
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_sign_up_view(client):
    get = client.get("/auth/sign_up/")
    delete = client.delete("/auth/sign_up/")
    assert get.status_code == 200
    assert delete.status_code == 405


@pytest.mark.django_db
def test_sign_up_with_existed_email(client, user):
    password = get_random_string
    response = client.post(
        "/auth/sign_up/",
        {
            "first_name": get_random_string(),
            "last_name": get_random_string(),
            "email": user.email,
            "password": password,
            "confirm_password": password,
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_sign_in_view(client):
    get = client.get("/auth/sign_in/")
    post = client.post("/auth/sign_in/")
    delete = client.delete("/auth/sign_in/")
    assert get.status_code == 200
    assert post.status_code == 400
    assert delete.status_code == 405


@pytest.mark.django_db
def test_sign_in_post_and_get_with_auth_user(client, user):
    user = UserFactory.create()
    password = get_random_string()
    user.set_password(password)
    user.is_confirmed = "CONFIRMED"
    user.save()
    response = client.post("/auth/sign_in/", {"email": user.email, "password": password})
    assert response.status_code == 302
    assert response["Location"] == reverse("root")
    response = client.get("/auth/sign_in/")
    assert response.status_code == 302
    assert response["Location"] == reverse("root")


@pytest.mark.django_db
def test_sign_in_with_auth_user_wrong_password_success(client, user):
    user = UserFactory.create()
    password = get_random_string()
    user.set_password(password)
    user.is_confirmed = "CONFIRMED"
    user.save()
    response = client.post("/auth/sign_in/", {"email": user.email, "password": password[::-1]})
    assert response.status_code == 400


@pytest.mark.django_db
def test_forgot_sign_in_with_not_registered_user_fail(client):
    response = client.post(
        "/auth/sign_in/",
        {
            "email": f"{get_random_string()}@{get_random_string()}.{get_random_string()}",
            "password": get_random_string(),
        },
    )
    assert response.status_code == 400
    response = client.post(
        "/auth/forgot/",
        {"email": f"{get_random_string()}@{get_random_string()}.{get_random_string()}"},
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_reset_with_registered_user_success(client, user):
    response = client.get("/auth/forgot/")
    assert response.status_code == 200
    client.post("/auth/forgot/", {"email": user.email})
    user = User.objects.get(email=user.email)
    new_password = get_random_string()
    response = client.post(
        "/auth/reset/",
        {
            "password": new_password,
            "confirm_password": new_password,
            "code": user.confirmation_code,
        },
    )
    assert response.status_code == 302
    assert response["Location"] == reverse("authentication:signIn")
    response = client.post("/auth/sign_in/", {"email": user.email, "password": new_password})
    assert response.status_code == 302
    assert response["Location"] == reverse("root")


@pytest.mark.django_db
def test_reset_with_registered_user_fail(client, user):
    user = User.objects.get(email=user.email)
    response = client.post(
        "/auth/reset/",
        {
            "password": get_random_string(),
            "confirm_password": get_random_string(),
            "code": user.confirmation_code,
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_reset_view_get_with_registered_user_success(client, user):
    response = client.get(f"/auth/reset/{user.confirmation_code}")
    assert response.status_code == 200
