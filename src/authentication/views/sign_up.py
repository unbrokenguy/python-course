from django.conf import settings
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from authentication.forms import SignUpForm
from authentication.tasks import send_email


class SignUpView(View):
    """
    Sign Up View.
    GET <url>/auth/sign_up/ - Return template registration.html
    POST <url>/auth/sign_up/ - Post form handler with RegisterForm
    """

    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, "authentication/signUp.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            html_message = render_to_string(
                template_name="authentication/mail.html",
                context=dict(
                    code=user.confirmation_code,
                    name=user.first_name,
                    server_url=settings.ALLOWED_HOSTS[0],
                ),
            )
            send_email.delay(
                subject="Confirm Email",
                html_message=html_message,
                recipient_list=[user.email],
            )
            return redirect(reverse("root"))
        else:
            return render(request, "authentication/signUp.html", {"form": form}, status=400)
