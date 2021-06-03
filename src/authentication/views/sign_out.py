from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


@login_required(login_url=reverse_lazy("authentication:signIn"), redirect_field_name=None)
def sign_out_view(request):
    logout(request)
    return redirect(reverse("authentication:signIn"))
