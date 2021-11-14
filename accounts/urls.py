from django.urls import path

from .views import  MyAccountView #, set_paid_until_view

urlpatterns = [
    path('my-account/', MyAccountView.as_view(), name='my_account'),
    # path('set-months/<int:months>/', set_paid_until_view, name='set_paid_until_view'),
]
