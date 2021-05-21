import json

import pytest
from django.utils.crypto import get_random_string

from core.tests.user_factory import UserFactory
from links.models import Link


@pytest.mark.django_db
def test_anonymous_link_create_success(client):
    response = client.post("/links/", {"expire_time": 0, "url": "https://google.com/"})
    assert response.status_code == 200
    assert json.loads(response.content).get("link")
    assert len(json.loads(response.content)["link"]) == 10


@pytest.mark.django_db
def test_user_link_create_success(client):
    user = UserFactory.create()
    user.set_password(get_random_string())
    user.is_confirmed = "CONFIRMED"
    user.save()
    client.force_login(user)
    response = client.post("/links/", {"expire_time": 0, "url": "https://google.com/"})
    assert response.status_code == 200
    assert Link.objects.get(creator=user).short_link == json.loads(response.content).get("link")
