import factory


class UserFactory(factory.django.DjangoModelFactory):
    username = "user"
    email = "user@email.com"
    password = "pass123"

    class Meta:
        model = "accounts.CustomUser"
        django_get_or_create = ("username",)


class SuperUserFactory(factory.django.DjangoModelFactory):
    username = "admin"
    email = "admin@email.com"
    password = factory.PostGenerationMethodCall("set_password", "admin")
    is_superuser = True
    is_staff = True
    is_active = True

    class Meta:
        model = "accounts.CustomUser"
        django_get_or_create = ("username",)
