from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods
from  django.shortcuts import redirect, render
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class MyAccountView(TemplateView):
    template_name = 'account/my_account.html'
