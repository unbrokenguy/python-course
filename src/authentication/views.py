from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.urls import reverse
from django.views import View
from authentication.models import send_email
from authentication.forms import LoginForm, RegisterForm
from authentication.models import User


class SignUpView(View):
    """
    Sign Up View.
    GET <url>/auth/sign_up/ - Return template registration.html
    POST <url>/auth/sign_up/ - Post form handler with RegisterForm
    """

    def get(self, request, *args, **kwargs):
        return render(request, "registration.html", {"form": RegisterForm()})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            try:
                validate_password(password, user)
            except ValidationError as e:
                form.add_error("password", e)
                return render(request, "registration.html", {"form": form, "errors": form.errors.values()}, status=400)
            user.set_password(password)
            user.save()
            send_email(
                subject="Confirm Email",
                template="mail.html",
                to_email=user.email,
                args=dict(code=user.confirmation_code, name=user.first_name),
            )
            return redirect(reverse("root"))
        else:
            return render(request, "registration.html", {"form": form})


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
        return render(request, "login.html", {"form": form})

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
                    "login.html",
                    {"form": form, "errors": ["Incorrect login or password or you need to confirm your account"]},
                )
        else:
            return redirect(reverse("authentication:signIn"))


class ConfirmView(View):
    def get(self, request, *args, **kwargs):
        success = False
        try:
            user = User.objects.get(confirmation_code=kwargs["code"])
            if user.is_confirmed == "NOT_CONFIRMED":
                user.is_confirmed = "CONFIRMED"
                user.save()
                success = True
        except ValidationError:
            success = False
        return render(request, "confirm.html", {"success": success})


@login_required(login_url=reverse_lazy("authentication:signIn"), redirect_field_name=None)
def logout_view(request):
    logout(request)
    return redirect(reverse("authentication:signIn"))
