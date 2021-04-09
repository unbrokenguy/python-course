import random
import string

from django.db import models


def generate_hash_salt(length: int = 50) -> str:
    """Generate random string to use it as a hash salt.
    Args:
        length: An Integer hash salt with 50 chars length.

    Returns:
        Random string with A-Z, a-z, 0-9 and special symbols.
    """
    return "".join(random.choice(string.ascii_letters +
                                 string.digits +
                                 string.punctuation) for _ in range(length))


class Link(models.Model):
    """Django ORM Model of link
    Attributes:
        origin_url: A string with origin url.
        short_link: A string with short url.
        views: An integer count of views.
    """
    origin_url = models.CharField(max_length=2083)
    short_link = models.CharField(max_length=255, unique=True)
    views = models.BigIntegerField(default=0)  # Temporary, need to be another model.


# TODO Views Model to store who and when viewed link.
