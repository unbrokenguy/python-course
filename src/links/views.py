from django.db.models import ProtectedError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from hashlib import sha256

from django.views.generic import ListView, RedirectView, CreateView, DeleteView

from links.forms import LinkForm
from links.models import Link, generate_hash_salt
from base64 import b64encode


class LinkListView(ListView):
    """
    GET request url: <server>/links/list/
    Returns:
        Rendered template links_list.html with links.
    # TODO update template page layout.
    """

    model = Link
    template_name = "link_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LinkRedirectView(RedirectView):

    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        """
        GET request url: <server>/<slug:short_link>/
        Args:
            request: Django Request object.
            *args: Positional args.
            **kwargs: Keyword args. {"short_url": r"[0-9a-zA-Z+_]{10}"}
                 short_url: A string with length 10 and in base64 alphabet.
        Redirects to origin url and , or send 404 http error if short_link doesn't exist.
        """
        link = get_object_or_404(Link, short_link=kwargs["short_link"])
        link.views += 1
        link.save()
        return link.origin_url


# TODO LinkDeleteView.
class LinkDeleteView(DeleteView):
    model = Link

    def delete(self, request, *args, **kwargs):
        """
        DELETE request url: <server>/links/<slug:short_url/
        Args:
            request: Django Request object.
            *args: Positional args.
            **kwargs: Keyword args. {"short_url": r"[0-9a-zA-Z+_]{10}"}
                short_url: A string with length 10 and in base64 alphabet.
        Returns:
            HttpResponse with status code 200 if deleted successfully or 404
        """
        link = get_object_or_404(self.model, short_link=kwargs["short_url"])
        try:
            link.delete()
        except ProtectedError:
            return HttpResponse("Link can't be deleted.", status=400)
        return HttpResponse(status=200)


class LinkCreateView(CreateView):
    create_template = "index.html"

    def get(self, request, *args, **kwargs):
        """
        GET request url: <server>/links/
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
        POST request to create short link. url: <server>/links/
        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        form = LinkForm(request.POST)
        if form.is_valid():
            _url = form.cleaned_data["url"]  # get url from post data
            hash_salt = generate_hash_salt()  # generate hash salt
            hash_func = sha256()  # hashing algorithm
            hash_func.update((_url + hash_salt).encode("utf-8"))  # hash url with salt
            short_link = hash_func.hexdigest()  # hash url with salt
            short_link = b64encode(bytes.fromhex(short_link)).decode()[:10]  # hex to base64 and slice first 10 chars
            short_link.replace("+", "-")
            short_link.replace("/", "_")
            Link.objects.create(origin_url=_url, short_link=short_link)
            data = {"link": short_link}
            return JsonResponse(data)
        data = {"error": "error"}
        return JsonResponse(data)
