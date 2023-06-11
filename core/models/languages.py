import deepl


import auto_prefetch

from django.db import models
from django.conf import settings
from django.conf.global_settings import LANGUAGES as DJANGO_LANGUAGES

from .secrets import Secrets


class Language(auto_prefetch.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=32, default="Other Language")
    is_source_in_deepl = models.BooleanField(default=False)
    is_target_in_deepl = models.BooleanField(default=False)
    supports_formality_in_deepl = models.BooleanField(default=False)
    use_in_faker = models.BooleanField(default=False)

    @classmethod
    def get(cls, code):
        return cls.objects.get_or_create(code=code)[0]

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
            translator = deepl.Translator(Secrets.get().deepl_auth_key)
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
