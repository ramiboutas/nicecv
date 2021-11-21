from django.urls import path

from .views import HomePageView, PrivacyPolicyView, TermsAndConditionsView, CookiePolicyView, GeneralFAQView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('cookie-policy/', CookiePolicyView.as_view(), name='cookie_policy'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms_and_conditions'),
    path('general-faq/', GeneralFAQView.as_view(), name='general_faq'),

]
