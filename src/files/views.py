import mimetypes
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from django.conf import settings
from files.forms import AttachmentForm
from files.models import Attachment
from links.models import Link, generate_short_link
from stats.utils import views_count_by_date_for_object


class AttachmentDownloadView(View):

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        """
        POST request
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
        file, file_name = open(f"{settings.MEDIA_ROOT}/{attachment.file}", "rb"), attachment.original_name

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


class AttachmentListView(LoginRequiredMixin, ListView):
    """
    GET request
    url: <server>/files/list/
    Returns:
        Rendered template files/list.html with links.
    """

    login_url = "/auth/sign_in/"
    redirect_field_name = None
    model = Attachment
    template_name = "files/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        user = self.request.user
        file = Attachment.objects.filter(
            creator=user,
        )
        return file


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
            file = Attachment(file=form.cleaned_data["file"], original_name=form.cleaned_data["file"].name)

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


class AttachmentDetailView(LoginRequiredMixin, DetailView):
    model = Attachment
    login_url = "/auth/sign_in/"
    redirect_field_name = None
    context_object_name = "file"
    template_name = "files/detail.html"

    def get_object(self, queryset=None):
        file = get_object_or_404(Attachment, creator=self.request.user, id=self.kwargs["pk"])
        self.extra_context = {"views": views_count_by_date_for_object(file)}
        return file
