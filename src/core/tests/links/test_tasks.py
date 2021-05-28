from datetime import timedelta

import pytest
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.utils.crypto import get_random_string

from core.tests.user_factory import UserFactory
from links.models import Link, generate_short_link
from links.tasks import delete_expired_anonymous_links


@pytest.mark.django_db
def test_delete_expired_anonymous_links_success():
    link = Link.objects.create(origin_url="https://google.com/", short_link=generate_short_link("https://google.com/"))

    permanent = Link.objects.create(
        origin_url="https://google.com/", short_link=generate_short_link("https://google.com/"), permanent=True
    )
    not_expired = Link.objects.create(
        origin_url="https://google.com/",
        short_link=generate_short_link("https://google.com/"),
        expire_time=timezone.now() + timedelta(days=7),
    )
    link.expire_time = timezone.now() + timedelta(days=-7)
    link.save()
    delete_expired_anonymous_links.apply()
    assert Link.objects.get(id=permanent.id)
    assert Link.objects.get(id=not_expired.id)
    with pytest.raises(ObjectDoesNotExist):
        Link.objects.get(id=link.id)


@pytest.mark.django_db
def test_delete_expired_user_links_fail(client):
    user = UserFactory.create()
    user.set_password(get_random_string())
    user.save()
    client.force_login(user)
    link = Link.objects.create(
        origin_url="https://google.com/", short_link=generate_short_link("https://google.com/"), creator=user
    )
    link.expire_time = timezone.now() + timedelta(days=-7)
    link.save()
    delete_expired_anonymous_links.apply()
    assert Link.objects.get(id=link.id)
