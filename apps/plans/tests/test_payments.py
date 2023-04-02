from django.test import RequestFactory

from apps.accounts.factories import UserFactory
from apps.plans.factories import PremiumPlanFactory
from apps.plans.payments import create_stripe_session
from config.test import TestCase


class StripeSessionTests(TestCase):
    def test_create_stripe_session(self):
        plan = PremiumPlanFactory()
        request = RequestFactory().get(plan.checkout_url)
        request.user = UserFactory()
        session = create_stripe_session(request, plan=plan)
        self.assertTrue("checkout.stripe.com" in session["url"])
        # stripe.error.InvalidRequestError:
        # Request req_J6xlGkgEKN9JF2: You passed an empty string for 'line_items[0][price_data][product_data][name]'.
        # We assume empty values are an attempt to unset a parameter; however 'line_items[0][price_data][product_data][name]' cannot be unset.
        # You should remove 'line_items[0][price_data][product_data][name]' from your request or supply a non-empty value.
