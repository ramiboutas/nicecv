import factory


class PremiumPlanFactory(factory.django.DjangoModelFactory):
    name = "Premium Plan"
    description = "This is a description of the plan"
    months = 3
    price = 10.0
    profile_translation = True

    class Meta:
        model = "core.PremiumPlan"
        django_get_or_create = ("months",)


class FreePlanFactory(factory.django.DjangoModelFactory):
    name = "Free Plan"
    description = "This is a description of the plan"

    class Meta:
        model = "core.FreePlan"
        django_get_or_create = ("name",)


class PlanFAQFactory(factory.django.DjangoModelFactory):
    question = "Is this a question?"
    answer = "Yes, it is."

    class Meta:
        model = "core.PlanFAQ"
        django_get_or_create = ("question",)
