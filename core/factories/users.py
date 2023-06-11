import factory

from ..factories.plans import PremiumPlanFactory


class UserFactory(factory.django.DjangoModelFactory):
    username = "user"
    email = "user@email.com"
    password = "pass123"

    class Meta:
        model = "core.User"
        django_get_or_create = ("username",)


class SuperUserFactory(factory.django.DjangoModelFactory):
    username = "admin"
    email = "admin@email.com"
    password = factory.PostGenerationMethodCall("set_password", "admin")
    is_superuser = True
    is_staff = True
    is_active = True

    class Meta:
        model = "core.User"
        django_get_or_create = ("username",)


class UserPremiumPlanFactory(factory.django.DjangoModelFactory):
    plan = factory.SubFactory(PremiumPlanFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = "core.UserPremiumPlan"
        django_get_or_create = ("user", "plan")
