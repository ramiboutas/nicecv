from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import Plan


def pricing_view(request):
    months = request.GET.get('months')
    try:
        plan = Plan.objects.get(months=months)
    except:
        plan = Plan.objects.filter(default=True).first() # first default plan
    month_list = Plan.objects.values_list('months', flat=True)
    context = {'plan': plan, 'months': month_list}
    return render(request, 'pricing/main.html', context)

@login_required
def hx_get_payment_methods_view(request):
    """
    This will be called just if the user is logged in (this logic is in the templates).
    We will return a partial of the payments methods
    """
    if request.htmx:
        return render(request, 'pricing/partials/payment-methods.html')
    return redirect('pricing_main')


@login_required
def get_payment_methods_view(request):
    """
    This function + the login_required decorator will be called when the user is not logged in. After loggin in, we redirect to the pricing page
    """
    return redirect('pricing_main')


def hx_update_price_view(request):
    if request.htmx:
        months = request.GET.get('months')
        plan = Plan.objects.filter(months=int(months)).first()
        context = {'plan': plan}
        return render(request, 'pricing/partials/price.html', context)
    return redirect('pricing_main')
