import mimetypes

from django.conf import settings
from django.db.models import F
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import View

from files.models import Attachment


class AttachmentDownloadView(View):

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        """
        GET request
        url: <server>/files/download/<slug:short_url/
        Args:
            request: Django Request object.
            *args: Positional args.
            **kwargs: Keyword args. {"short_url": r"[0-9a-zA-Z+_]{10}"}
                 short_url: String.
        Returns:
            FileResponse with file if file exist successfully or 404
        """
        attachment = get_object_or_404(Attachment, short_url=kwargs.get("short_url"))
        if attachment.file_exist is False:
            raise Http404
        if attachment.permanent is False and timezone.now() > attachment.expire_time:
            raise Http404
        # if attachment is not permanent and expired return 404
        file, file_name = (
            open(f"{settings.MEDIA_ROOT}/{attachment.file}", "rb"),
            attachment.original_name,
        )

        # We need to define headers so attachment will be download with its original name
        # If we use FileResponse file name will be uuid4
        response = HttpResponse(
            file,
            headers={
                "Content-Type": mimetypes.guess_type(file_name)[0],
                "Content-Disposition": f'attachment; filename="{file_name}"',
            },
            status=200,
        )

        if attachment.one_off:  # If attachment is one off we need to delete it.
            attachment.delete()
        else:  # If attachment is not one off we need to collect statistics
            attachment.views.create(date=timezone.now().date())
            attachment.downloads = F("downloads") + 1
            attachment.save()

        return response
