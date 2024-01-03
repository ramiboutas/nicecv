from django.urls import path

from ..views.users import (
    account_dashboard,
    account_edit,
    redirect_change_password,
    account_delete,
)


urlpatterns = [
    path("account/", account_dashboard, name="account_dashboard"),
    path("account/edit/", account_edit, name="account_edit"),
    path("account/delete/<int:id>/", account_delete, name="account_delete"),
    path("<int:id>/password/", redirect_change_password),
]
