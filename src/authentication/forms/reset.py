from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class ResetForm(forms.Form):
    """
    Reset password Form
    Attributes:
        password: String with new password.
        confirm_password: String with new password.
        code: uuid4 User confirmation code
    """

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    code = forms.UUIDField(widget=forms.HiddenInput(), required=True)

    def clean(self):
        """
        Cleans form data and check if password equal confirm_password
        Raises:
            ValidationError if passwords are not the same.
        """
        cleaned_data = super(ResetForm, self).clean()
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        validate_password(password)
        if password != confirm_password:
            self.add_error("confirm_password", "Passwords are not the same.")
            raise ValidationError("Error occurred")
        return cleaned_data
