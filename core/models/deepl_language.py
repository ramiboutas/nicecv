import auto_prefetch
import deepl
from django.conf import settings
from django.db import models

from .secrets import Secrets


class DeeplLanguage(auto_prefetch.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=32)
    is_source = models.BooleanField(default=False)
    is_target = models.BooleanField(default=False)
    supports_formality = models.BooleanField(default=False)

    @classmethod
    def get(cls, code):
        return cls.objects.get_or_create(code=code)[0]

    @classmethod
    def get_default(clas):
        return clas.objects.get_or_create(code=settings.LANGUAGE_CODE)[0]

    @classmethod
    def update_objects(cls):
        try:
            translator = deepl.Translator(Secrets.get().deepl_auth_key)
        except Exception as e:
            print(f"🔴 Error setting up Deepl translator: {e}")
            return

        for language in translator.get_source_languages():
            obj, _ = cls.objects.get_or_create(code=language.code.lower())
            obj.name = language.name
            obj.is_source = True
            obj.save()
            print(f"✅ {obj} created.")

        for language in translator.get_target_languages():
            obj, _ = cls.objects.get_or_create(code=language.code.lower())
            obj.name = language.name
            obj.supports_formality = language.supports_formality
            obj.is_target = True
            obj.save()
            print(f"✅ {obj} created.")

    def __str__(self) -> str:
        return f"Language ({self.code} - {self.name})"
