from django.contrib import admin
from django.urls import include, path

from links.views import LinkCreateView, LinkRedirectView

urlpatterns = [
    path("", LinkCreateView.as_view(), name="root"),
    path("admin/", admin.site.urls),
    path(
        "auth/",
        include(("authentication.urls", "authentication"), namespace="authentication"),
    ),
    path("links/", include(("links.urls", "links"), namespace="links")),
    path("files/", include(("files.urls", "files"), namespace="files")),
    path("<slug:short_link>/", LinkRedirectView.as_view()),
]
