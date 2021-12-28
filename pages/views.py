from django.views.generic import TemplateView
from django.shortcuts import redirect, render


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profiles_list')
        return render(self.request, self.template_name)


class PrivacyPolicyView(TemplateView):
    template_name = 'pages/privacy-policy.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'pages/terms-conditions.html'


class CookiePolicyView(TemplateView):
    template_name = 'pages/cookie-policy.html'

class GeneralFAQView(TemplateView):
    template_name = 'pages/faq-general.html'
