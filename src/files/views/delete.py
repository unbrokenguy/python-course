from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from files.models import Attachment


class AttachmentDeleteView(LoginRequiredMixin, View):

    login_url = "/auth/sign_in/"
    redirect_field_name = None
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        """
        POST request
        url: <server>/files/<int:pk/
        Args:
            request: Django Request object.
            *args: Positional args.
            **kwargs: Keyword args. {"pk": int"}
                 pk: Primary Key.
        Returns:
            HttpResponse with status code 200 if deleted successfully or 404
        """
        file = get_object_or_404(Attachment, id=kwargs["pk"])
        if file.creator.id == request.user.id:
            file.delete()
            return HttpResponse(reverse("files:list"), status=200)
        else:
            return HttpResponse(status=403)
