import factory


class ResumeTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "tex.ResumeTemplate"
        django_get_or_create = ("name",)
