__all__ = [
    "AttachmentListView",
    "AttachmentDeleteView",
    "AttachmentDownloadView",
    "AttachmentDetailView",
    "AttachmentCreateView",
]

from files.views.create import AttachmentCreateView
from files.views.delete import AttachmentDeleteView
from files.views.detail import AttachmentDetailView
from files.views.download import AttachmentDownloadView
from files.views.list import AttachmentListView
