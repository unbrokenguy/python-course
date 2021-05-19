import uuid

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.template.loader import render_to_string


class NoUserNameUserManager(UserManager):
    """
    Custom User manager to make username == email.
    """
    def create_superuser(self, email=None, password=None, **extra_fields):
        super().create_superuser(username=email, email=email, password=password)


class ConfirmStateEnum(models.TextChoices):
    CONFIRMED = "CONFIRMED"
    NOT_CONFIRMED = "NOT_CONFIRMED"


class User(AbstractUser):
    """
    User Django ORM model, inherits from AbstractUser
    """
    email = models.EmailField(blank=True, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = NoUserNameUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = self.email
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

    confirmation_code = models.UUIDField(default=uuid.uuid4(), editable=False)
    is_confirmed = models.CharField(max_length=255,
                                    choices=ConfirmStateEnum.choices,
                                    default=ConfirmStateEnum.NOT_CONFIRMED)


def send_email(subject, from_email, to_email, template, args):

    html_message = render_to_string(template, args)
    send_mail(subject=subject, message='', from_email=from_email,
              recipient_list=[to_email], html_message=html_message)
