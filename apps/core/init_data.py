from apps.accounts.factories import SuperUserFactory
from apps.plans.factories import PremiumPlanFactory


def create_initial_objects():
    SuperUserFactory()
    PremiumPlanFactory()
    PremiumPlanFactory(price=14, months=6)
