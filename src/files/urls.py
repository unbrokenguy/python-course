from django.urls import path

from files.views import (
    AttachmentCreateView,
    AttachmentDeleteView,
    AttachmentDetailView,
    AttachmentDownloadView,
    AttachmentListView,
)

urlpatterns = [
    path("", AttachmentCreateView.as_view(), name="create"),
    path("list/", AttachmentListView.as_view(), name="list"),
    path("<int:pk>/", AttachmentDetailView.as_view(), name="detail"),
    path("delete/<int:pk>/", AttachmentDeleteView.as_view(), name="delete"),
    path("download/<slug:short_url>/", AttachmentDownloadView.as_view(), name="download"),
]
