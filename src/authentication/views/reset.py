from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from authentication.forms import ResetForm
from authentication.models import User


class ResetView(View):
    """
    Reset password View.
    GET <url>/auth/reset/<code:uuid4>/ - Return template reset.html with ResetForm.
    POST <url>/auth/reset/ - Post ResetForm handler.
    """

    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        form = ResetForm()
        form.fields["code"].initial = kwargs.get("code")
        return render(request, "authentication/reset.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ResetForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, confirmation_code=form.cleaned_data["code"])
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect(reverse("authentication:signIn"))
        else:
            return render(request, "authentication/reset.html", {"form": form}, status=400)
