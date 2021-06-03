from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import RedirectView

from links.models import Link


class LinkRedirectView(RedirectView):

    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        """
        GET request
        url: <server>/<slug:short_link>/
        Args:
            request: Django Request object.
            *args: Positional args.
            **kwargs: Keyword args. {"short_link": r"[0-9a-zA-Z_-]{10}"}
                 short_link: A string with length 10 and in base64 alphabet.
        Redirects to origin url and , or send 404 http error if short_link doesn't exist.
        """
        link = get_object_or_404(Link, short_link=kwargs["short_link"])
        if link.permanent or link.expire_time >= timezone.now():
            if link.creator:
                link.views.create(date=timezone.now().date())
                link.save()
            return link.origin_url
        raise Http404
