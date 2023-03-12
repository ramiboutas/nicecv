import factory

from accounts.factories import UserFactory


class PremiumPlanFactory(factory.django.DjangoModelFactory):
    months = 3
    price = 10.0

    class Meta:
        model = "plans.PremiumPlan"
        django_get_or_create = ("months",)


class PlanFAQFactory(factory.django.DjangoModelFactory):
    question = "Is this a question?"
    answer = "Yes, it is."

    class Meta:
        model = "plans.PlanFAQ"
        django_get_or_create = ("question",)


class OrderFactory(factory.django.DjangoModelFactory):
    plan = factory.SubFactory(PremiumPlanFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = "plans.Order"
        django_get_or_create = ("plan", "user")
