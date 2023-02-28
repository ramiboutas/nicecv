import stripe

from django.utils.translation import gettext_lazy as _
from django.db.models import Model
from django.conf import settings

from subscriptions.models import Order
from subscriptions.models import Plan


def fulfill_order(user_id:int=None, plan_id:int=None):
    # fulfills the order and assigns premium to user.
    if user_id and plan_id:
        try:
            plan = Plan.objects.get(id=plan_id)
            user = User.objects.get(id=user_id)
            Order(plan=plan, user=user).save()
            user.set_paid_until(plan.months)
        
        except User.DoesNotExist:
            pass
        
        except Plan.DoesNotExist:
            pass


def create_stripe_session(plan: Model):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        # customer_email = request.user.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'EUR',
                    'product_data': {
                    'name': str(plan.months) + _(' months subscription to premium (no renewal)'),
                    },
                    'unit_amount': int(plan.price * 100),
                },
                'quantity': 1,
            },
        ],
        metadata={"plan_id": plan.id, "user_id": request.user.id},
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payments_success')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('payments_failed')),
    )
    print()
    return session
    