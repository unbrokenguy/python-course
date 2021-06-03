from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from links.models import Link
from stats.utils import views_count_by_date_for_object


class LinkDetailView(LoginRequiredMixin, DetailView):
    model = Link

    login_url = "/auth/sign_in/"
    redirect_field_name = None

    context_object_name = "link"
    template_name = "links/detail.html"

    def get_object(self, queryset=None):
        link = get_object_or_404(Link, creator=self.request.user, id=self.kwargs["pk"])
        views = views_count_by_date_for_object(link)
        self.extra_context = {"views": views, "summary": sum(views.values())}
        return link
