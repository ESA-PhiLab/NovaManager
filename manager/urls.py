from django.contrib.auth.decorators import login_required
from django.urls import path, include

from manager.views import MachinesView, TurnOnView, TurnOffView

urlpatterns = [
    path("", login_required(MachinesView.as_view(), login_url="/accounts/login/")),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "turn_on/<str:instance>/",
        login_required(TurnOnView.as_view(), login_url="/accounts/login/"),
        name="turn_on",
    ),
    path(
        "turn_off/<str:instance>/",
        login_required(TurnOffView.as_view(), login_url="/accounts/login/"),
        name="turn_off",
    ),
]
