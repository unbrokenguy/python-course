from celery.schedules import crontab
from celery.task import periodic_task
from django.utils import timezone

from links.models import Link


@periodic_task(run_every=crontab(minute=0, hour=0))
def delete_expired_anonymous_links():
    for link in Link.objects.all():
        if link.creator is None:
            if link.permanent is False and link.expire_time <= timezone.now():
                link.delete()
