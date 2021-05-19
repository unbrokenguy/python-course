from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.urls import reverse

from authentication.models import send_email
from authentication.forms import LoginForm, RegisterForm
from authentication.models import User


def login_view(request):
    if request.method == "GET":
        return login_get(request)
    if request.method == "POST":
        return login_post(request)
    return HttpResponse(status=405)


def login_post(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password"])
        if user is not None and user.is_confirmed == "CONFIRMED":
            login(request, user)
            return redirect(reverse('root'))
        else:
            return render(
                request, "login.html",
                {"form": form, "errors": ["Incorrect login or password or you need to confirm your account"]})
    else:
        return redirect(reverse("authentication:signIn"))


def login_get(request):
    if request.user.is_authenticated:
        return redirect(reverse('root'))
    form = LoginForm()
    return render(request, "login.html", {"form": form})


@login_required(login_url=reverse_lazy('authentication:signIn'), redirect_field_name=None)
def logout_view(request):
    logout(request)
    return redirect(reverse("authentication:signIn"))


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            try:
                validate_password(password, user)
            except ValidationError as e:
                form.add_error("password", e)
                return render(request, "registration.html", {'form': form, "errors": form.errors.values()}, status=400)
            user.set_password(password)
            user.save()
            login(request, user)
            send_email("Confirm Email", settings.DEFAULT_FROM_EMAIL, user.email,
                       'mail.html', args=dict(code=user.confirmation_code, name=user.first_name))
            return redirect(reverse("root"))
        else:
            return render(request, "registration.html", {"form": form})
    else:
        return render(request, "registration.html", {"form": RegisterForm()})


def confirm(request, code):
    success = False
    if request.method == "GET":
        try:
            user = User.objects.get(code=code)
            if user.is_confirmed == "NOT_CONFIRMED":
                user.is_confirmed = "CONFIRMED"
                user.save()
                success = True
        except ValidationError:
            success = False
        return render(request, "confirm.html", {"success": success})
