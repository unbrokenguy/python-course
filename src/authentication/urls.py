from django.urls import path
from authentication.views import login_view, register_view, confirm, logout_view

urlpatterns = [
    path('sign_in/', login_view, name="signIn"),
    path('sign_up/', register_view, name="signUp"),
    path('sign_out/', logout_view, name="signOut"),
    path(r'confirm/(?P<code>[\w-]+)$', confirm, name='confirm'),
]
