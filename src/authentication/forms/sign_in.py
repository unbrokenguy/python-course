from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from authentication.models import User


class SignInForm(forms.Form):
    """
    Sign In Form
    Attributes:
        email: String with user email.
        password: String with user password.
    """

    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        """
        Clean email field and check if User with given email exists or
        User confirmed his account
        Raises:
            ValidationError if user does not exist or
                or did not confirm his account.
        """
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ValidationError("User with this email doesn't Exists.")
        if user.is_confirmed != "CONFIRMED":
            raise ValidationError("You have not verified your account.")
        return email

    def clean_password(self):
        """
        Clean password field and check it to be strong.
        Raises:
            ValidationError if password is too weak.
        """
        password = self.cleaned_data["password"]
        validate_password(password)
        return password
