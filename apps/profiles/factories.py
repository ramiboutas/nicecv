import factory

from apps.core.models import Language


faked_language = Language.fake_object()


class ProfileFactory(factory.django.DjangoModelFactory):
    fullname = factory.Faker("name", locale=faked_language.code)
    jobtitle = factory.Faker("job", locale=faked_language.code)
    location = factory.Faker("city", locale=faked_language.code)
    phone = factory.Faker("phone_number", locale=faked_language.code)
    email = factory.Faker("email", locale=faked_language.code)
    about = factory.Faker("text", locale=faked_language.code)
    category = "template"
    language_setting = faked_language
    full_photo = factory.django.ImageField()
    cropped_photo = factory.django.ImageField()
    # crop_x = models.PositiveSmallIntegerField(**null_blank)
    # crop_y = models.PositiveSmallIntegerField(**null_blank)
    # crop_width = models.PositiveSmallIntegerField(**null_blank)
    # crop_height = models.PositiveSmallIntegerField(**null_blank)

    class Meta:
        model = "profiles.Profile"
        # django_get_or_create = ("id",)


class SkillFactory(factory.django.DjangoModelFactory):
    profile = factory.SubFactory(ProfileFactory)
    name = "Excel"

    class Meta:
        model = "profiles.Skill"
