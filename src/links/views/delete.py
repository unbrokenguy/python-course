from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from links.models import Link


class LinkDeleteView(LoginRequiredMixin, View):

    login_url = "/auth/sign_in/"
    redirect_field_name = None
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        """
        POST request
        url: <server>/links/<int:pk>/
        Args:
            request: Django Request object.
            *args: Positional args.
            **kwargs: Keyword args. {"pk": Integer"}
                pk: Primary key.
        Returns:
            HttpResponse with status code 200 if deleted successfully or 404
        """
        link = get_object_or_404(Link, id=kwargs["pk"])
        if link.creator.id == request.user.id:
            link.delete()
            return HttpResponse(reverse("links:list"), status=200)
        else:
            return HttpResponse(status=403)
