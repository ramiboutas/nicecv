from django.urls import path

from ..views.users import MyAccountView

app_name = "users"

urlpatterns = [
    path("me/", MyAccountView.as_view(), name="dashboard"),
]
