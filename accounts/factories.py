import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounts.CustomUser" 
        django_get_or_create = ("username",)


    username = "user"
    email = "user@email.com"
    password = "pass123"


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounts.CustomUser" 
        django_get_or_create = ("username",)

    username = "superuser"
    email = "superuser@email.com"
    password = factory.PostGenerationMethodCall('set_password', 'pass123')
    is_superuser = True
    is_staff = True
    is_active = True