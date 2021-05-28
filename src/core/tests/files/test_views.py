import json
from datetime import timedelta

import pytest
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string

from core.tests.files.test_tasks import random_picture
from core.tests.user_factory import UserFactory
from files.models import Attachment
from links.models import generate_short_link, Link


@pytest.fixture
def user():
    user = UserFactory.create()
    user.set_password(get_random_string())
    user.is_confirmed = "CONFIRMED"
    user.save()
    return user


@pytest.mark.django_db
def test_attachment_anonymous_list_view(client):
    response = client.get("/files/list/")
    assert response.status_code == 302
    assert response["Location"] == reverse("authentication:signIn")


@pytest.mark.django_db
def test_attachment_user_list_view(client, user):
    client.force_login(user)
    response = client.get("/files/list/")
    assert response.status_code == 200
    assert "No files yet." in response.content.decode("utf-8")


@pytest.mark.django_db
def test_attachment_anonymous_delete_view(client):
    response = client.post("/files/delete/1/")
    assert response.status_code == 302
    assert response["Location"] == reverse("authentication:signIn")


@pytest.mark.django_db
def test_attachment_user_delete_view(client, user):
    file = random_picture()
    attachment = Attachment(
        file=file, original_name=file.name, expire_time=timezone.now() + timedelta(days=7), creator=user
    )

    url = f"https://{settings.ALLOWED_HOSTS[0]}/files/download/"
    short_url = generate_short_link(url + attachment.original_name)
    new_url = url + short_url + "/"
    attachment.short_url = short_url

    link = Link(permanent=True, origin_url=new_url, short_link=short_url)
    link.save()
    attachment.save()

    # another user try to delete.
    another_user = UserFactory.create()
    another_user.set_password(get_random_string())
    another_user.is_confirmed = "CONFIRMED"
    another_user.save()
    client.force_login(another_user)
    response = client.post(f"/files/delete/{attachment.id}/")
    assert response.status_code == 403
    client.logout()
    # creator try to delete.
    client.force_login(user)
    response = client.post(f"/files/delete/{attachment.id}/")
    assert response.status_code == 200
    with pytest.raises(ObjectDoesNotExist):
        Attachment.objects.get(id=attachment.id)


@pytest.mark.django_db
def test_files_get_create_view(client, user):
    anonymous = client.get("/files/")
    client.force_login(user)
    authenticated = client.get("/files/")
    assert anonymous.status_code == 200
    assert authenticated.status_code == 200
    assert "Sign In." in anonymous.content.decode("utf-8")
    assert "Sign Out." in authenticated.content.decode("utf-8")


@pytest.mark.django_db
def test_files_post_anonymous_create_view(client):
    anonymous = client.post("/files/", {"file": random_picture(), "expire_time": -1})
    assert anonymous.status_code == 200
    attachment = Attachment.objects.get(short_url=json.loads(anonymous.content.decode("utf-8"))["link"])
    assert attachment.one_off
    assert attachment.creator is None


@pytest.mark.django_db
@pytest.mark.parametrize("expire_time", [-1, 0, 1, 7])
def test_files_post_user_create_view_success(client, user, expire_time):
    client.force_login(user)
    response = client.post("/files/", {"file": random_picture(), "expire_time": expire_time})
    attachment = Attachment.objects.get(short_url=json.loads(response.content.decode("utf-8"))["link"])

    assert response.status_code == 200
    if expire_time == 0:
        assert attachment.permanent is True
    elif expire_time == -1:
        assert attachment.one_off is True
    else:
        assert attachment.expire_time.strftime("%Y-%m-%d %H:%M") == (
            timezone.now() + timedelta(days=expire_time)
        ).strftime("%Y-%m-%d %H:%M")
    assert attachment.creator.email == user.email


@pytest.mark.django_db
def test_files_post_user_create_view_fail(client, user):

    one_week = client.post(
        "/files/",
        {"random_parameter": get_random_string(), "second_random_parameter": get_random_string(), "expire_time": 7},
    )
    assert one_week.status_code == 200
    assert json.loads(one_week.content.decode("utf-8")).get("error")
    client.force_login(user)
    wrong_expire_time = client.post("/files/", {"file": random_picture(), "expire_time": 30})
    assert wrong_expire_time.status_code == 200
    assert json.loads(wrong_expire_time.content.decode("utf-8")).get("error")


@pytest.mark.django_db
def test_files_user_detail_view(client, user):
    client.force_login(user)
    response = client.post("/files/", {"file": random_picture(), "expire_time": -1})
    attachment = Attachment.objects.get(short_url=json.loads(response.content.decode("utf-8"))["link"])
    response = client.get(f"/files/{attachment.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("expire_time", [-1, 0, 1, 7, "file_deleted"])
def test_files_user_download_view(client, user, expire_time):
    client.force_login(user)

    short_url = json.loads(
        client.post(
            "/files/", {"file": random_picture(), "expire_time": 0 if expire_time == "file_deleted" else expire_time}
        ).content.decode("utf-8")
    )["link"]

    response = client.get(f"/files/download/{short_url}/")
    assert response.status_code == 200

    status_code = 404
    if expire_time != -1:
        attachment = Attachment.objects.get(short_url=short_url)
        if expire_time == "file_deleted":
            attachment.file_exist = False
        else:
            attachment.expire_time += timedelta(days=-100)
            if expire_time == 0:
                status_code = 200
        attachment.save()
    response = client.get(f"/files/download/{short_url}/")
    assert response.status_code == status_code
