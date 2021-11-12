from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'pages/privacy-policy.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'pages/terms-conditions.html'
