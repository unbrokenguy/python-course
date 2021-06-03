import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


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

    confirmation_code = models.UUIDField(default=uuid.uuid4(), editable=False)
    is_confirmed = models.CharField(
        max_length=255,
        choices=ConfirmStateEnum.choices,
        default=ConfirmStateEnum.NOT_CONFIRMED,
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = self.email
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
