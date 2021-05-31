from django.utils import timezone

from core.celery import app
from links.models import Link


@app.task
def delete_expired_anonymous_links():
    for link in Link.objects.all():
        if link.creator is None:
            if link.permanent is False and link.expire_time <= timezone.now():
                link.delete()
