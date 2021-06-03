from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from files.models import Attachment


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
