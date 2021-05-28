from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_email(subject, html_message, recipient_list):
    send_mail(
        subject=subject,
        message=None,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
    )
