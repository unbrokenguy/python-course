__all__ = [
    "SignUpView",
    "SignInView",
    "ConfirmView",
    "ForgotView",
    "ResetView",
    "sign_out_view",
]

from authentication.views.confirm import ConfirmView
from authentication.views.forgot import ForgotView
from authentication.views.reset import ResetView
from authentication.views.sign_in import SignInView
from authentication.views.sign_out import sign_out_view
from authentication.views.sign_up import SignUpView
