from accounts.factories import SuperUserFactory
from plans.factories import PlanFactory


def create_initial_objects():
    SuperUserFactory()
    PlanFactory()
    PlanFactory(price=14, months=6)
