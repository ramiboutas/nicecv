import factory


class PremiumPlanFactory(factory.django.DjangoModelFactory):
    name = "Premium Plan"
    description = "This is a description of the plan"
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
