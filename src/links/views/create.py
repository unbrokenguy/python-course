from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import CreateView

from links.forms import LinkForm
from links.models import Link, generate_short_link


class LinkCreateView(CreateView):
    create_template = "links/create.html"

    def get(self, request, *args, **kwargs):
        """
        GET request
        url: <server>/links/
        Args:
            request: Django Request object.
            *args: Positional args.
            **kwargs: Keyword args.
        Returns:
            Rendered template index.html with LinkForm.
        """
        form = LinkForm()
        return render(request, self.create_template, {"form": form})

    def post(self, request, *args, **kwargs):
        """
        POST request to create short link.
        url: <server>/links/
        Args:
            request: Django Request object with LinkForm data.
            *args: Positional args.
            **kwargs: Keyword args.
        Returns:
            JsonResponse with link if no errors occurred else message with error
        """
        form = LinkForm(request.POST)
        if form.is_valid():
            _url = form.cleaned_data["url"]  # get url from post data
            _short_link = generate_short_link(_url)
            _expire_time = int(form.cleaned_data["expire_time"])  # get expire_time from post data
            link = Link.objects.create(origin_url=_url, short_link=_short_link)
            if _expire_time == 0:
                link.permanent = True
            else:
                link.expire_time = timezone.now() + timedelta(days=_expire_time)
            if request.user.is_authenticated:
                link.creator = request.user  # if user is authenticated add creator to link
            link.save()
            data = {"link": _short_link}
            return JsonResponse(data)
        data = {"error": form.errors}
        return JsonResponse(data)
