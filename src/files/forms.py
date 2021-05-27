from django import forms
from django.core.validators import RegexValidator

day_validator = RegexValidator(r"(-1|0|1|7)", "Link is alive only once, one day or week, or unlimited time.")

CHOICES = (
    (-1, "One off"),
    (0, "Unlimited"),
    (1, "One day"),
    (7, "One week"),
)


class AttachmentForm(forms.Form):
    """
    Django Form of models.Link class
    Attributes:
        file: A field with file, required.
        expire_time: When link will be expire.
    """

    file = forms.FileField(required=True)
    expire_time = forms.ChoiceField(widget=forms.Select(), choices=CHOICES)
