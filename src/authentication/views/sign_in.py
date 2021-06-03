from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from authentication.forms import SignInForm


class SignInView(View):
    """
    Sign In View.
    GET <url>/auth/sign_in/ - Return template login.html
    POST <url>/auth/sign_in/ - Post form handler with LoginForm
    """

    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("root"))
        form = SignInForm()
        return render(request, "authentication/signIn.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if not user:
                form.add_error(field="password", error="Password is not correct.")
                return render(request, "authentication/signIn.html", {"form": form}, status=400)
            login(request, user)
            return redirect(reverse("root"))
        else:
            return render(request, "authentication/signIn.html", {"form": form}, status=400)
