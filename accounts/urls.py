from django.urls import path

from .views import  MyAccountView, early_adopters_view #, set_paid_until_view

urlpatterns = [
    path('my-account/', MyAccountView.as_view(), name='my_account'),
    path('early-adopters/', early_adopters_view, name='accounts_early_adopters_url'),
    # path('set-months/<int:months>/', set_paid_until_view, name='set_paid_until_view'),
]
