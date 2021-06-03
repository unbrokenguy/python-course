from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from authentication.models import User


class SignUpForm(forms.ModelForm):
    """
    Sign In Form
    Attributes:
        first_name: String with user first name.
        last_name: String with user last name.
        email: String with user email.
        password: String with user password.
        confirm_password: String with user password.
    """

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean(self):
        """
        Cleans form data and check
        validate the password
        if password equal confirm_password
        Raises:
            ValidationError if passwords are not the same or password is too weak.
        """
        cleaned_data = super(SignUpForm, self).clean()
        try:
            email = cleaned_data["email"]
            password = cleaned_data["password"]
            confirm_password = cleaned_data["confirm_password"]
            validate_password(password)
            if password == email:
                raise ValidationError("Passwords and email are the same.")
            if password != confirm_password:
                raise ValidationError("Passwords are not the same.")
            return cleaned_data
        except KeyError:
            raise ValidationError("All fields required.")

    def clean_email(self):
        """
        Clean email field and check if User with given email exists.
        Raises:
            ValidationError if user exists.
        """
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            self.add_error("email", "User with this email Already Exists.")
            raise ValidationError("Error occurred.")
        return email

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
