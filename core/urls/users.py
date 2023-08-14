from django.urls import path

from ..views.users import account_dashboard
from ..views.users import account_edit
from ..views.users import redirect_change_password


urlpatterns = [
    path("account/", account_dashboard, name="account_dashboard"),
    path("account/edit/", account_edit, name="account_edit"),
    path("<int:id>/password/", redirect_change_password),
]
