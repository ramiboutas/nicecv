import deepl
import random


from django.db import models
from django.db import IntegrityError
from django.conf.global_settings import LANGUAGES as DJANGO_LANGUAGES

from django.conf import settings


# Create your models here.


class Settings(models.Model):
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
        return cls.objects.get_or_create(singleton=True)[0]


class Language(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=32, default="Other Language")
    is_source_in_deepl = models.BooleanField(default=False)
    is_target_in_deepl = models.BooleanField(default=False)
    supports_formality_in_deepl = models.BooleanField(default=False)
    use_in_faker = models.BooleanField(default=False)

    @classmethod
    def fake_object(cls):
        return random.choice(list(cls.objects.filter(use_in_faker=True)))

    @classmethod
    def create_initial_objects(cls):
        # Languages available in Django global settings
        for code, name in DJANGO_LANGUAGES:
            obj, _ = cls.objects.get_or_create(code=code)
            obj.name = name
            obj.use_in_faker = code in [lang[0] for lang in settings.LANGUAGES]
            obj.save()
            print(f"✅ {obj} created.")

        # Languages in deepl
        try:
            translator = deepl.Translator(Settings.get().deepl_auth_key)
        except Exception as e:
            print(f"🔴 Error setting up Deepl translator: {e}")
            return

        for language in translator.get_source_languages():
            obj, _ = cls.objects.get_or_create(code=language.code.lower())
            obj.name = language.name
            obj.use_in_faker = code in [lang[0] for lang in settings.LANGUAGES]
            obj.is_source_in_deepl = True
            obj.save()
            print(f"✅ {obj} created.")

        for language in translator.get_target_languages():
            obj, _ = cls.objects.get_or_create(code=language.code.lower())
            obj.use_in_faker = code in [lang[0] for lang in settings.LANGUAGES]
            obj.name = language.name
            obj.supports_formality_in_deepl = language.supports_formality
            obj.is_target_in_deepl = True
            obj.save()
            print(f"✅ {obj} created.")

    @classmethod
    def get_deepl_objects(cls):
        return cls.objects.filter(available_in_deepl=True)

    def __str__(self) -> str:
        return f"Language ({self.code} - {self.name})"
