from datetime import timedelta

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import CreateView

from files.forms import AttachmentForm
from files.models import Attachment
from links.models import Link, generate_short_link


class AttachmentCreateView(CreateView):
    create_template = "files/create.html"

    def get(self, request, *args, **kwargs):
        """
        GET request
        url: <server>/files/
        Args:
            request: Django Request object.
            *args: Positional args.
            **kwargs: Keyword args.
        Returns:
            Rendered template files/create.html with AttachmentForm.
        """
        form = AttachmentForm()
        return render(request, self.create_template, {"form": form})

    def post(self, request, *args, **kwargs):
        """
        POST request to create file.
        url: <server>/files/
        Args:
            request: Django Request object with AttachmentForm data and Files.
            *args: Positional args.
            **kwargs: Keyword args.
        Returns:
            JsonResponse with link if no errors occurred else message with error
        """
        data = None
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            file = Attachment(
                file=form.cleaned_data["file"],
                original_name=form.cleaned_data["file"].name,
            )

            url = f"https://{settings.ALLOWED_HOSTS[0]}/files/download/"
            short_url = generate_short_link(url + file.original_name)
            url = url + short_url + "/"

            file.short_url = short_url
            link = Link(permanent=True, origin_url=url, short_link=short_url)

            expire_time = -1
            if request.user.is_authenticated:
                file.creator = request.user
                expire_time = int(form.cleaned_data["expire_time"])

            if expire_time == -1:
                file.one_off = True
                file.permanent = True
            elif expire_time == 0:
                file.permanent = True
            else:
                file.expire_time = timezone.now() + timedelta(days=expire_time)

            file.save()
            link.save()

            data = {"link": short_url}

        data = data or {"error": form.errors}
        return JsonResponse(data)
