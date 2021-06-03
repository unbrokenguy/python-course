import uuid

from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View

from authentication.forms import ForgotForm
from authentication.models import User
from authentication.tasks import send_email


class ForgotView(View):
    """
    Forgot password View.
    GET <url>/auth/forgot/ - Return template forgot.html with ForgotForm.
    POST <url>/auth/forgot/ - Post ForgotForm handler, send forgot_mail to given email.
    """

    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        form = ForgotForm()
        return render(request, "authentication/forgot.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ForgotForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data["email"])
            user.confirmation_code = uuid.uuid4()
            user.save()
            html_message = render_to_string(
                template_name="authentication/forgot_mail.html",
                context=dict(
                    code=user.confirmation_code,
                    name=user.first_name,
                    server_url=settings.ALLOWED_HOSTS[0],
                ),
            )
            send_email.delay(
                subject="Reset password.",
                html_message=html_message,
                recipient_list=[user.email],
            )
            return render(
                request,
                "authentication/forgot.html",
                {"form": form, "status": "Email sent successfully."},
                status=200,
            )
        else:
            return render(request, "authentication/forgot.html", {"form": form}, status=400)
