from django.urls import path, re_path

from authentication.views import ConfirmView, SignInView, SignUpView, logout_view

urlpatterns = [
    path("sign_in/", SignInView.as_view(), name="signIn"),
    path("sign_up/", SignUpView.as_view(), name="signUp"),
    path("sign_out/", logout_view, name="signOut"),
    re_path(r"confirm/(?P<code>[\w-]+)$", ConfirmView.as_view(), name="confirm"),
]
