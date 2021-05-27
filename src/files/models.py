import uuid

from django.db import models
from django.utils import timezone

from authentication.models import User
from stats.models import StatView


def file_upload(_, filename: str) -> str:
    new_filename = ".".join((str(uuid.uuid4()), filename.split(".")[-1]))
    return f"attachments/{new_filename}"


class Attachment(models.Model):
    """Django ORM Model of link
    Attributes:
        file: A string with origin url.
        creator: User who created link.
        short_link: A string with short url.
        expire_time: Datetime field when link need to be deleted.
        permanent: Boolean if True File will always be available.
        one_off: Boolean if True File will be available once.
        views: ManyToMany Field to StatView, (list of views).
        downloads: Integer with number of downloads.
    """

    file = models.FileField(upload_to=file_upload, null=False)
    original_name = models.CharField(max_length=255)

    short_url = models.CharField(max_length=255, unique=True)

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    expire_time = models.DateTimeField(default=timezone.now)
    permanent = models.BooleanField(default=False)
    one_off = models.BooleanField(default=False)

    views = models.ManyToManyField(StatView)
    downloads = models.IntegerField(default=0)
