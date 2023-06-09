from django.db import models
from django.db import IntegrityError
from django.conf.global_settings import LANGUAGES as DJANGO_LANGUAGES

# Create your models here.


class Setting(models.Model):
    """https://github.com/shangxiao/stupid-django-tricks/tree/master/singleton_models"""

    singleton = models.BooleanField(primary_key=True, default=True)
    name = models.CharField(max_length=32, default="API keys and dynamic settings")
    # linkedin
    linkedin_client_id = models.CharField(max_length=255, blank=True)
    linkedin_client_secret = models.CharField(max_length=255, blank=True)
    linkedin_profile_id = models.CharField(max_length=255, blank=True)
    linkedin_access_token = models.CharField(max_length=255, blank=True)
    linkedin_organization_id = models.CharField(max_length=255, blank=True)
    linkedin_organization_access_token = models.CharField(max_length=255, blank=True)
    linkedin_organization_refresh_token = models.CharField(max_length=255, blank=True)

    # twitter
    twitter_username = models.CharField(max_length=255, blank=True)
    twitter_client_id = models.CharField(max_length=255, blank=True)
    twitter_client_secret = models.CharField(max_length=255, blank=True)
    twitter_api_key = models.CharField(max_length=255, blank=True)
    twitter_api_key_secret = models.CharField(max_length=255, blank=True)
    twitter_access_token = models.CharField(max_length=255, blank=True)
    twitter_access_token_secret = models.CharField(max_length=255, blank=True)
    twitter_bearer_token = models.CharField(max_length=255, blank=True)

    # facebook
    facebook_page_id = models.CharField(max_length=255, blank=True)
    facebook_page_access_token = models.CharField(max_length=255, blank=True)
    facebook_app_id = models.CharField(max_length=255, blank=True)
    facebook_app_secret_key = models.CharField(max_length=255, blank=True)

    # instagram
    instagram_page_id = models.CharField(max_length=255, blank=True)
    instagram_access_token = models.CharField(max_length=255, blank=True)

    # deepl api
    deepl_auth_key = models.CharField(max_length=255, blank=True)

    class Meta:
        constraints = (
            models.CheckConstraint(
                name="single_setting_model",
                check=models.Q(singleton=True),
            ),
        )

    @classmethod
    def get(cls):
        return cls.objects.get_or_create(the_singleton=True)[0]


class Language(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=32, default="Other Language")
    available_in_deepl = models.BooleanField(default=False)
    deepl_formality = models.BooleanField(
        verbose_name="Support formality on Deepl", default=False
    )

    @classmethod
    def create_initial_objects(cls):
        # TODO: create from available languages in deepl
        # https://github.com/DeepLcom/deepl-python#listing-available-languages
        objects = []
        for code, name in DJANGO_LANGUAGES:
            objects.append(cls(code=code, name=name))
        try:
            cls.objects.bulk_create(objects)
            print("✅ Languages created")
        except IntegrityError:
            print("✅ Languages were already created")

    @classmethod
    def get_deepl_objects(cls):
        return cls.objects.filter(available_in_deepl=True)

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"
