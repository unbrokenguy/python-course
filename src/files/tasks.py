import os

from celery.schedules import crontab
from celery.task import periodic_task
from django.utils import timezone
from django.conf import settings
from files.models import Attachment


@periodic_task(run_every=crontab(minute=0, hour=0))
def delete_expired_files():
    for attachment in Attachment.objects.all():
        if attachment.permanent is False and attachment.expire_time < timezone.now():
            attachment.file_exist = False
            attachment.save()
            os.remove(f"{settings.MEDIA_ROOT}/{attachment.file}")
