from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from authentication.models import User


class ForgotForm(forms.Form):
    """
    Forgot password Form
    Attributes:
        email: String with user email who wants to reset password.
    """

    email = forms.EmailField()

    def clean_email(self):
        """
        Cleans form data and check if user with given email exists
        Raises:
            ValidationError if User does not exist.
        """
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ValidationError("User with this email doesn't Exists.")
        return email
