from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from links.models import Link


class LinkListView(LoginRequiredMixin, ListView):
    """
    GET request
    url: <server>/links/list/
    Returns:
        Rendered template links_list.html with links.
    """

    login_url = "/auth/sign_in/"
    redirect_field_name = None
    model = Link
    template_name = "links/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        user = self.request.user
        links = Link.objects.filter(
            creator=user,
        )
        return links
