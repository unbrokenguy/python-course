import json
from datetime import timedelta

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.crypto import get_random_string

from core.tests.user_factory import UserFactory
from links.models import Link, generate_short_link


@pytest.fixture
def user():
    user = UserFactory.create()
    user.set_password(get_random_string())
    user.is_confirmed = "CONFIRMED"
    user.save()
    return user


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
    link = Link.objects.create(
        origin_url="https://google.com/",
        short_link=generate_short_link("https://google.com/"),
    )
    link.expire_time = timezone.now() + timedelta(days=-7)
    link.save()
    response = client.get(f"/{link.short_link}/")
    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize("expire_time", [0, 1, 7])
def test_link_detail_view(client, user, expire_time):
    # anonymous
    response = client.post("/", {"expire_time": expire_time, "url": "https://google.com/"})
    link = Link.objects.get(short_link=json.loads(response.content.decode("utf-8"))["link"])
    assert client.get(f"/links/{link.id}/").status_code == 302

    # authenticated
    client.force_login(user)
    response = client.post("/", {"expire_time": expire_time, "url": "https://google.com/"})
    link = Link.objects.get(short_link=json.loads(response.content.decode("utf-8"))["link"])
    response = client.get(f"/links/{link.id}/")
    assert response.status_code == 200
    assert link.short_link in response.content.decode("utf-8")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "form",
    [
        {"ur1": 10, "expire_time": 0},
        {"expire_time": 30, "url": "https://google.com/"},
    ],
)
def test_link_create_view_form_fail(client, form):
    response = client.post("/", form)
    assert response.status_code == 200
    assert json.loads(response.content.decode("utf-8")).get("error")


@pytest.mark.django_db
def test_links_create_view_get_success(client):
    response = client.get("/links/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_links_delete_view(client, user):
    client.force_login(user)
    response = client.post("/", {"expire_time": 0, "url": "https://google.com/"})
    client.logout()
    # anonymous
    link = Link.objects.get(short_link=json.loads(response.content.decode("utf-8"))["link"])
    response = client.post(f"/links/delete/{link.id}/")
    assert response.status_code == 302

    # another user
    another_user = UserFactory.create()
    another_user.set_password(get_random_string())
    another_user.is_confirmed = "CONFIRMED"
    another_user.save()
    client.force_login(another_user)
    response = client.post(f"/links/delete/{link.id}/")
    assert response.status_code == 403
    client.logout()

    # creator
    client.force_login(user)
    response = client.post("/", {"expire_time": 0, "url": "https://google.com/"})
    link = Link.objects.get(short_link=json.loads(response.content.decode("utf-8"))["link"])
    response = client.post(f"/links/delete/{link.id}/")
    assert response.status_code == 200
    with pytest.raises(ObjectDoesNotExist):
        Link.objects.get(id=link.id)
