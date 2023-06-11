import factory


class ResumeTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "core.ResumeTemplate"
        django_get_or_create = ("name",)
