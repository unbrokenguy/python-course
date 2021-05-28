from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, RedirectView

from links.forms import LinkForm
from links.models import Link, generate_short_link
from stats.utils import views_count_by_date_for_object


class LinkListView(LoginRequiredMixin, ListView):
    """
    GET request
    url: <server>/links/list/
    Returns:
        Rendered template links_list.html with links.
    """

    login_url = "/auth/sign_in/"
    redirect_field_name = "redirect_to"
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


class LinkRedirectView(RedirectView):

    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        """
        GET request
        url: <server>/<int:pk>/
        Args:
            request: Django Request object.
            *args: Positional args.
            **kwargs: Keyword args. {"pk": int"}
                 pk: Primary Key.
        Redirects to origin url and , or send 404 http error if short_link doesn't exist.
        """
        link = get_object_or_404(Link, short_link=kwargs["short_link"])
        if link.permanent or link.expire_time >= timezone.now():
            link.views.create(date=timezone.now().date())
            link.save()
            return link.origin_url
        raise Http404


class LinkDeleteView(LoginRequiredMixin, View):

    login_url = "/auth/sign_in/"
    redirect_field_name = "redirect_to"
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        """
        POST request
        url: <server>/links/<slug:short_url/
        Args:
            request: Django Request object.
            *args: Positional args.
            **kwargs: Keyword args. {"short_url": r"[0-9a-zA-Z+_]{10}"}
                short_url: A string with length 10 and in base64 alphabet.
        Returns:
            HttpResponse with status code 200 if deleted successfully or 404
        """
        link = get_object_or_404(Link, id=kwargs["pk"])
        if link.creator.id == request.user.id:
            try:
                link.delete()
                return HttpResponse(reverse("links:list"), status=200)
            except ProtectedError:
                return HttpResponse("Link can't be deleted.", status=400)
        else:
            return HttpResponse(status=403)


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
            request:
            *args:
            **kwargs:
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
            elif _expire_time == 1 or _expire_time == 7:
                link.expire_time = timezone.now() + timedelta(days=_expire_time)
            if request.user.is_authenticated:
                link.creator = request.user  # if user is authenticated add creator to link
            link.save()
            data = {"link": _short_link}
            return JsonResponse(data)
        data = {"error": form.errors}
        return JsonResponse(data)


class LinkDetailView(DetailView):
    model = Link
    context_object_name = "link"
    template_name = "links/detail.html"

    def get_object(self, queryset=None):
        link = get_object_or_404(Link, creator=self.request.user, id=self.kwargs["pk"])
        views = views_count_by_date_for_object(link)
        self.extra_context = {"views": views, "summary": sum(views.values())}
        return link
