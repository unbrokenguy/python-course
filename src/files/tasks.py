import os

from django.utils import timezone
from django.conf import settings

from core.celery import app
from files.models import Attachment


@app.task
def delete_expired_files():
    for attachment in Attachment.objects.all():
        if attachment.permanent is False and attachment.expire_time < timezone.now():
            attachment.file_exist = False
            attachment.save()
            os.remove(f"{settings.MEDIA_ROOT}/{attachment.file}")
