from django.urls import path

from links.views import LinkCreateView, LinkDeleteView, LinkDetailView, LinkListView

urlpatterns = [
    path("", LinkCreateView.as_view(), name="create"),
    path("list/", LinkListView.as_view(), name="list"),
    path("<int:pk>/", LinkDetailView.as_view(), name="detail"),
    path("delete/<int:pk>/", LinkDeleteView.as_view(), name="delete"),
]
