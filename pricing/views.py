from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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


# move to a payments app!
def proceed_with_payment_view(request):
    payment_method = request.POST.get("payment_method")
    if payment_method == "card":
        return HttpResponse("this will return a stripe page")
    elif payment_method == "paypal":
        return HttpResponse("this will return a paypal page")
    elif payment_method == "coinbase":
        return HttpResponse("this will return a coinbase page")
    return HttpResponse("somethin wrong happend :(")




# https://testdriven.io/blog/django-coinbase/


# https://nicecv.online/pricing/payment/stripe/webhook/


# app.py
#
# Use this sample code to handle webhook events in your integration.
#
# 1) Paste this code into a new file (app.py)
#
# 2) Install dependencies
#   pip3 install flask
#   pip3 install stripe
#
# 3) Run the server on http://localhost:4242
#   python3 -m flask run --port=4242

# import json
# import os
# import stripe
#
# from flask import Flask, jsonify, request
#
# # This is your Stripe CLI webhook secret for testing your endpoint locally.
# endpoint_secret = 'whsec_Y532PlnmUecVPMCTFbEF0ASv24kxrv6c'
#
# app = Flask(__name__)
#
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     event = None
#     payload = request.data
#     sig_header = request.headers['STRIPE_SIGNATURE']
#
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         raise e
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         raise e
#
#     # Handle the event
#     if event['type'] == 'checkout.session.async_payment_failed':
#       session = event['data']['object']
#     elif event['type'] == 'checkout.session.async_payment_succeeded':
#       session = event['data']['object']
#     elif event['type'] == 'checkout.session.completed':
#       session = event['data']['object']
#     elif event['type'] == 'checkout.session.expired':
#       session = event['data']['object']
#     elif event['type'] == 'invoice.created':
#       invoice = event['data']['object']
#     elif event['type'] == 'invoice.deleted':
#       invoice = event['data']['object']
#     elif event['type'] == 'invoice.finalization_failed':
#       invoice = event['data']['object']
#     elif event['type'] == 'invoice.finalized':
#       invoice = event['data']['object']
#     elif event['type'] == 'invoice.marked_uncollectible':
#       invoice = event['data']['object']
#     elif event['type'] == 'invoice.paid':
#       invoice = event['data']['object']
#     elif event['type'] == 'invoice.payment_action_required':
#       invoice = event['data']['object']
#     elif event['type'] == 'invoice.payment_failed':
#       invoice = event['data']['object']
#     elif event['type'] == 'invoice.payment_succeeded':
#       invoice = event['data']['object']
#     elif event['type'] == 'invoice.sent':
#       invoice = event['data']['object']
#     elif event['type'] == 'invoice.upcoming':
#       invoice = event['data']['object']
#     elif event['type'] == 'invoice.updated':
#       invoice = event['data']['object']
#     elif event['type'] == 'invoice.voided':
#       invoice = event['data']['object']
#     elif event['type'] == 'payment_intent.amount_capturable_updated':
#       payment_intent = event['data']['object']
#     elif event['type'] == 'payment_intent.canceled':
#       payment_intent = event['data']['object']
#     elif event['type'] == 'payment_intent.created':
#       payment_intent = event['data']['object']
#     elif event['type'] == 'payment_intent.payment_failed':
#       payment_intent = event['data']['object']
#     elif event['type'] == 'payment_intent.processing':
#       payment_intent = event['data']['object']
#     elif event['type'] == 'payment_intent.requires_action':
#       payment_intent = event['data']['object']
#     elif event['type'] == 'payment_intent.succeeded':
#       payment_intent = event['data']['object']
#     elif event['type'] == 'payout.canceled':
#       payout = event['data']['object']
#     elif event['type'] == 'payout.created':
#       payout = event['data']['object']
#     elif event['type'] == 'payout.failed':
#       payout = event['data']['object']
#     elif event['type'] == 'payout.paid':
#       payout = event['data']['object']
#     elif event['type'] == 'payout.updated':
#       payout = event['data']['object']
#     # ... handle other event types
#     else:
#       print('Unhandled event type {}'.format(event['type']))
#
#     return jsonify(success=True)
