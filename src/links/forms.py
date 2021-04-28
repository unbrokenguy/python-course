from django import forms


class LinkForm(forms.Form):
    """
    Django Form of models.Link class
    Attributes:
        url: A string with url, required.
    """

    url = forms.CharField(widget=forms.URLInput, required=True)
