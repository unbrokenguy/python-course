from django.shortcuts import get_object_or_404, render
from django.views import View

from authentication.models import User


class ConfirmView(View):

    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        success = False
        user = get_object_or_404(User, confirmation_code=kwargs["code"])
        if user.is_confirmed == "NOT_CONFIRMED":
            user.is_confirmed = "CONFIRMED"
            user.save()
            success = True
        return render(request, "authentication/confirm.html", {"success": success})
