import os
from datetime import timedelta
from io import BytesIO
from random import randint

import pytest
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.utils import timezone
from django.utils.crypto import get_random_string
from PIL import Image

from files.models import Attachment
from files.tasks import delete_expired_files
from links.models import Link, generate_short_link


def random_picture():
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    size = (randint(100, 1000), randint(20, 1000))
    name = get_random_string()
    file_obj = BytesIO()
    image = Image.new("RGBA", size=size, color=color)
    image.save(file_obj, "png")
    file_obj.seek(0)
    return ContentFile(file_obj.read(), f"{name}.png")


@pytest.mark.django_db
def test_delete_expired_files():
    url = f"https://{settings.ALLOWED_HOSTS[0]}/files/download/"

    pic_to_delete = random_picture()
    file_to_delete = Attachment(
        file=pic_to_delete,
        original_name=pic_to_delete.name,
        expire_time=timezone.now() + timedelta(days=-7),
    )

    file_path_to_delete = file_to_delete.file

    short_url = generate_short_link(url + file_to_delete.original_name)
    new_url = url + short_url + "/"
    file_to_delete.short_url = short_url
    file_to_delete.save()

    link = Link(permanent=True, origin_url=new_url, short_link=short_url)
    link.save()

    pic_not_to_delete = random_picture()
    file_not_to_delete = Attachment(
        file=pic_not_to_delete,
        original_name=pic_not_to_delete.name,
        expire_time=timezone.now() + timedelta(days=7),
    )

    short_url = generate_short_link(url + file_not_to_delete.original_name)
    new_url = url + short_url + "/"

    file_not_to_delete.short_url = short_url
    file_not_to_delete.save()

    link = Link(permanent=True, origin_url=new_url, short_link=short_url)
    link.save()
    delete_expired_files.apply()

    assert os.path.exists(f"{settings.MEDIA_ROOT}/{file_path_to_delete}") is False

    file_to_delete = Attachment.objects.get(id=file_to_delete.id)
    assert file_to_delete.file_exist is False

    file_to_delete.delete()
    file_not_to_delete.delete()

    with pytest.raises(ObjectDoesNotExist):
        Link.objects.get(short_link=short_url)
