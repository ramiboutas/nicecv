import braintree

from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model

from .forms import SelectMonthPlanForm, LifeTimePlanForm
from .models import Plan


def pricing_view(request):
    plan = Plan.objects.filter(default=True).first() # first default plan
    print(plan)
    context = {'plan': plan}
    return render(request, 'pricing/plan_list.html', context)


@login_required
def checkout_view(request):
    #generate all other required data that you may need on the #checkout page and add them to context.
    months = request.POST.get('months')
    plan = get_object_or_404(Plan, months=months)

    if settings.BRAINTREE_PRODUCTION:
        braintree_env = braintree.Environment.Production
    else:
        braintree_env = braintree.Environment.Sandbox

    # Configure Braintree
    braintree.Configuration.configure(
        braintree_env,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY,
    )

    try:
        braintree_client_token = braintree.ClientToken.generate({'customer_id': request.user.id})
    except Exception as e:
        # SOLVE THIS!!!!! 
        print("----------")
        print(e)
        print("----------")
        braintree_client_token = braintree.ClientToken.generate({})

    context = {'braintree_client_token': braintree_client_token}

    return render(request, 'pricing/checkout.html', context)

@login_required
def payment_view(request):
    nonce_from_the_client = request.POST['paymentMethodNonce']
    customer_kwargs = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
    }
    customer_create = braintree.Customer.create(customer_kwargs)
    customer_id = customer_create.customer.id
    result = braintree.Transaction.sale({
        "amount": "10.00",
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })
    print(result)
    return HttpResponse('Ok')
