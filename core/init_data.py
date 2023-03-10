from plans.factories import PlanFactory
from accounts.factories import SuperUserFactory


def create_initial_objects():
    SuperUserFactory()
    PlanFactory()
    PlanFactory(price=14, saving=4, default=True)