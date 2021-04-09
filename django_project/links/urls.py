from django.urls import path
from links.views import LinkCreateView, LinkListView, LinkDeleteView


urlpatterns = [
    path('', LinkCreateView.as_view(), name='create'),
    path('list/', LinkListView.as_view(), name='list'),
    path('<slug:short_url>/', LinkDeleteView.as_view(), name='delete'),
]
