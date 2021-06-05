from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")


app.conf.beat_schedule = {
    "delete-expired-files-every-day": {
        "task": "tasks.delete_expired_files",
        "schedule": crontab(minute=0, hour=0),
    },
    "delete-expired-anonymous-links-every-day": {
        "task": "tasks.delete_expired_anonymous_links",
        "schedule": crontab(minute=0, hour=0),
    },
}

app.conf.timezone = "UTC"

app.autodiscover_tasks()
