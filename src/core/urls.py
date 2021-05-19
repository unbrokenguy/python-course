from django.contrib import admin
from django.urls import path, include
from links.views import LinkRedirectView, LinkCreateView
from links.urls import urlpatterns as links_urls


urlpatterns = [
    path("", LinkCreateView.as_view(), name="root"),
    path("admin/", admin.site.urls),
    path("auth/", include(("authentication.urls", "authentication"), namespace="authentication")),
    path("links/", include(links_urls), name="links"),
    path("<slug:short_link>/", LinkRedirectView.as_view()),
]
