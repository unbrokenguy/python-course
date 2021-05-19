import pytest
from django.urls import reverse
from django.utils.crypto import get_random_string
from core.tests.user_factory import UserFactory


def test_login_view(client):
    get = client.get("/auth/sign_in/")
    post = client.post("/auth/sign_in/")
    delete = client.delete("/auth/sign_in/")
    assert delete.status_code == 405
    assert get.status_code == 200
    assert post.status_code == 302


@pytest.mark.django_db
def test_sign_in_post_and_get_with_auth_user(client):
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
