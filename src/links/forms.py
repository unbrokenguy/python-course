from django import forms
from django.core.validators import RegexValidator

day_validator = RegexValidator(r"(0|1|7)", "Link is alive only one day, one week or unlimited time.")

CHOICES = (
    (0, "Unlimited"),
    (1, "One day"),
    (7, "One week"),
)


class LinkForm(forms.Form):
    """
    Django Form of models.Link class
    Attributes:
        url: A string with url, required.
        expire_time: When link will be expire.
    """

    url = forms.CharField(widget=forms.URLInput, required=True)
    expire_time = forms.ChoiceField(widget=forms.Select(), choices=CHOICES)
