from django.views.generic import TemplateView


class UserDashboard(TemplateView):
    template_name = "account/my_account.html"
