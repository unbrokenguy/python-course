import random
import string
from base64 import b64encode
from hashlib import sha256

from django.db import models
from django.utils import timezone

from authentication.models import User
from stats.models import StatView


def generate_hash_salt(length: int = 50) -> str:
    """Generate random string to use it as a hash salt.
    Args:
        length: An Integer hash salt with 50 chars length.

    Returns:
        Random string with A-Z, a-z, 0-9 and special symbols.
    """
    return "".join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))


def generate_short_link(origin_url):
    hash_salt = generate_hash_salt()  # generate hash salt
    hash_func = sha256()  # hashing algorithm
    hash_func.update((origin_url + hash_salt).encode("utf-8"))  # hash url with salt
    short_link = hash_func.hexdigest()  # hash url with salt
    short_link = b64encode(bytes.fromhex(short_link)).decode()[:10]  # hex to base64 and slice first 10 chars
    short_link = short_link.replace("+", "-")
    short_link = short_link.replace("/", "_")
    return short_link


class Link(models.Model):
    """Django ORM Model of link
    Attributes:
        origin_url: A string with origin url.
        short_link: A string with short url.
        expire_time: Datetime field when link need to be deleted.
        creator: User who created link.
        permanent: Boolean if True Link will always be available.
        views: ManyToMany Field to StatView, (list of views).
    """

    origin_url = models.CharField(max_length=2083)
    short_link = models.CharField(max_length=255, unique=True)

    expire_time = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    permanent = models.BooleanField(default=False)

    views = models.ManyToManyField(StatView)
