from django.urls import path

from ..views.users import MyAccountView

app_name = "users"

urlpatterns = [
    path("my-account/", MyAccountView.as_view(), name="my_account"),
]
