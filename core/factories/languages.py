import factory


class LanguageFactory(factory.django.DjangoModelFactory):
    code = "en"

    class Meta:
        model = "core.Language"
        django_get_or_create = ("code",)
