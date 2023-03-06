import factory

from accounts.factories import UserFactory




class PlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "subscriptions.Plan" 
        django_get_or_create = ("months",)

    months = 3
    default = False
    price = 10.0
    saving = 2.0
    stripe_product_id = "111"


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "subscriptions.Order"
        django_get_or_create = ("plan", "user")
    
    plan = PlanFactory()
    user = UserFactory()
