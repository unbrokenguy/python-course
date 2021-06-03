from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from files.models import Attachment
from stats.utils import views_count_by_date_for_object


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
