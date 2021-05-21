from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from core.settings import ALLOWED_HOSTS
from authentication.forms import LoginForm, RegisterForm
from authentication.models import User, send_email


class SignUpView(View):
    """
    Sign Up View.
    GET <url>/auth/sign_up/ - Return template registration.html
    POST <url>/auth/sign_up/ - Post form handler with RegisterForm
    """

    def get(self, request, *args, **kwargs):
        return render(request, "authentication/signUp.html", {"form": RegisterForm()})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            try:
                validate_password(password, user)
            except ValidationError as e:
                form.add_error("password", e)
                return render(
                    request, "authentication/signUp.html", {"form": form, "errors": form.errors.values()}, status=400
                )
            user.set_password(password)
            user.save()
            send_email(
                subject="Confirm Email",
                template="authentication/mail.html",
                to_email=user.email,
                args=dict(code=user.confirmation_code, name=user.first_name, server_url=ALLOWED_HOSTS[0]),
            )
            return redirect(reverse("root"))
        else:
            return render(request, "authentication/signUp.html", {"form": form})


class SignInView(View):
    """
    Sign In View.
    GET <url>/auth/sign_in/ - Return template login.html
    POST <url>/auth/sign_in/ - Post form handler with LoginForm
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("root"))
        form = LoginForm()
        return render(request, "authentication/signIn.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["email"], password=form.cleaned_data["password"])
            if user is not None and user.is_confirmed == "CONFIRMED":
                login(request, user)
                return redirect(reverse("root"))
            else:
                return render(
                    request,
                    "authentication/signIn.html",
                    {"form": form, "errors": ["Incorrect login or password or you need to confirm your account"]},
                )
        else:
            return redirect(reverse("authentication:signIn"))


class ConfirmView(View):
    def get(self, request, *args, **kwargs):
        success = False
        user = get_object_or_404(User, confirmation_code=kwargs["code"])
        if user.is_confirmed == "NOT_CONFIRMED":
            user.is_confirmed = "CONFIRMED"
            user.save()
            success = True
        return render(request, "authentication/confirm.html", {"success": success})


@login_required(login_url=reverse_lazy("authentication:signIn"), redirect_field_name=None)
def logout_view(request):
    logout(request)
    return redirect(reverse("authentication:signIn"))
