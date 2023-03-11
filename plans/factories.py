import factory

from accounts.factories import UserFactory


class PlanFactory(factory.django.DjangoModelFactory):
    months = 3
    price = 10.0

    class Meta:
        model = "plans.Plan"
        django_get_or_create = ("months",)


class OrderFactory(factory.django.DjangoModelFactory):
    plan = factory.SubFactory(PlanFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = "plans.Order"
        django_get_or_create = ("plan", "user")
