from django.contrib import admin
from django.urls import path, include
from links.views import LinkRedirectView
from links.urls import urlpatterns as links_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('links/', include(links_urls), name='links'),
    path('<slug:short_link>/', LinkRedirectView.as_view())
]
