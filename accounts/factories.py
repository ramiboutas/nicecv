import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounts.CustomUser" 
        django_get_or_create = ("username",)


    username = "user"
    email = "user@email.com"
    password = "pass123"
