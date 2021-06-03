from django.urls import path, re_path

from authentication.views import (
    ConfirmView,
    ForgotView,
    ResetView,
    SignInView,
    SignUpView,
    sign_out_view,
)

urlpatterns = [
    path("sign_in/", SignInView.as_view(), name="signIn"),
    path("sign_up/", SignUpView.as_view(), name="signUp"),
    path("sign_out/", sign_out_view, name="signOut"),
    path("forgot/", ForgotView.as_view(), name="forgot"),
    re_path(r"reset/(?P<code>[\w-]+)?$", ResetView.as_view(), name="reset"),
    re_path(r"confirm/(?P<code>[\w-]+)$", ConfirmView.as_view(), name="confirm"),
]
