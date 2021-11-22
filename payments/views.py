import stripe

from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# https://nicecv.online/pricing/payment/stripe/webhook/
# https://testdriven.io/blog/django-coinbase/

# declarations
stripe.api_key=settings.STRIPE_SECRET_KEY

@login_required
def proceed_with_payment_view(request):
    payment_method = request.POST.get('payment_method')
    if payment_method == "card":
        return stripe_checkout_view(request)
    elif payment_method == "paypal":
        return paypal_checkout_view(request)
    elif payment_method == "coinbase":
        return coinbase_checkout_view(request)
    messages.error(request, _('Somethig wrong happed, please try again or later'))
    return redirect('pricing_main')

def stripe_checkout_view(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email='customer@example.com',
            billing_address_collection='auto',
            line_items=[
                {
                    # Provide the exact Price ID (e.g. pr_1234) of the product you want to sell
                    'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)




def paypal_checkout_view(request):
    return HttpResponse("This wiew will proceed with paypal session")

def coinbase_checkout_view(request):
    return HttpResponse("This wiew will proceed with coinbase session")