from django.views.generic import TemplateView



class MyAccountView(TemplateView):
    template_name = 'account/my_account.html'
