import os

from django.utils import timezone
from django.conf import settings
from core.celery import app
from files.models import Attachment
from links.models import Link


@app.task
def delete_expired_files():
    for attachment in Attachment.objects.all():
        if attachment.permanent is False and attachment.expire_time <= timezone.now():
            attachment.file_exist = False
            attachment.save()
            link = Link.objects.get(short_link=attachment.short_url)
            link.delete()
            os.remove(f"{settings.MEDIA_ROOT}/{attachment.file}")
