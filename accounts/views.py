from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods
from  django.shortcuts import redirect, render
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import EarlyAdopter


class MyAccountView(TemplateView):
    template_name = 'account/my_account.html'


@require_http_methods(["POST"])
def early_adopters_view(request):
    email = request.POST.get('email')
    try:
        validate_email(email)
        EarlyAdopter.objects.create(email=email)
        return render(request, 'early_adopters_thanks.html')
    except ValidationError as e:
        messages.error(request, _('Enter a valid email'))
        return redirect('home')
    else:
        return redirect('home')





# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.shortcuts import redirect
#
# @login_required
# def set_paid_until_view(request, months):
#     user = request.user
#     user.set_paid_until(months)
#     messages.info(request, "You paid the pro for {months} months. Thank you!")
#     return redirect('home')
