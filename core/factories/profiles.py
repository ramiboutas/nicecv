import factory


class ProfileFactory(factory.django.DjangoModelFactory):
    fullname = factory.Faker("name")
    jobtitle = factory.Faker("job")
    location = factory.Faker("city")
    phone = factory.Faker("phone_number")
    email = factory.Faker("email")
    about = factory.Faker("text")
    category = "template"
    full_photo = factory.django.ImageField()
    cropped_photo = factory.django.ImageField()
    auto_created = True

    class Meta:
        model = "core.Profile"


class SkillFactory(factory.django.DjangoModelFactory):
    profile = factory.SubFactory(ProfileFactory)
    name = "Excel"

    class Meta:
        model = "core.Skill"
