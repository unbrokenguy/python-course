import json
from datetime import timedelta

import pytest
from django.utils import timezone
from django.utils.crypto import get_random_string

from core.tests.user_factory import UserFactory
from links.models import Link, generate_short_link


@pytest.mark.django_db
def test_link_list_view(client):
    user = UserFactory.create()
    user.set_password(get_random_string())
    user.save()
    not_auth_get = client.get("/links/list/")
    assert not_auth_get.status_code == 302
    client.force_login(user)
    auth_get = client.get("/links/list/")
    assert auth_get.status_code == 200


@pytest.mark.django_db
def test_link_redirect_view_success(client):
    response = client.post("/links/", {"expire_time": 0, "url": "https://google.com/"})
    response = client.get(f"/{json.loads(response.content)['link']}/")
    assert response.status_code == 302
    assert response["Location"] == "https://google.com/"


@pytest.mark.django_db
def test_link_redirect_view_fail(client):
    response = client.get("/0000000000/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_link_redirect_view_expire_time_fail(client):
    link = Link.objects.create(origin_url="https://google.com/", short_link=generate_short_link("https://google.com/"))
    link.expire_time = timezone.now() + timedelta(days=-7)
    link.save()
    response = client.get(f"/{link.short_link}/")
    assert response.status_code == 404
