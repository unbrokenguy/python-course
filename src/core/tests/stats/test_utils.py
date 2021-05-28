import pytest
from django.utils import timezone
from django.utils.crypto import get_random_string

from core.tests.user_factory import UserFactory
from links.models import Link, generate_short_link
from stats.utils import views_count_by_date_for_object


@pytest.mark.django_db
def test_views_count_by_date_for_object(client):
    user = UserFactory.create()
    user.is_confirmed = True
    user.set_password(get_random_string())
    user.save()
    client.force_login(user)

    link = Link.objects.create(
        origin_url="https://google.com/",
        short_link=generate_short_link("https://google.com/"),
        permanent=True,
        creator=user,
    )
    link.save()
    result = views_count_by_date_for_object(link)

    # No views.
    assert result == {}

    # 10 views.
    for i in range(10):
        client.get(f"/{link.short_link}/")
    link = Link.objects.get(id=link.id)
    result = views_count_by_date_for_object(link)
    assert result == {str(timezone.now().date()): 10}
