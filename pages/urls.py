from django.urls import path

from .views import HomePageView, PrivacyPolicyView, TermsAndConditionsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-conditions/', TermsAndConditionsView.as_view(), name='terms-conditions'),

]
