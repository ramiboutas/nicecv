from django.urls import path

from ..views.users import UserDashboard


urlpatterns = [
    path("account/", UserDashboard.as_view(), name="user_dashboard"),
]
