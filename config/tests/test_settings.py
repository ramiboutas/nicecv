from django.conf import settings
from django.test import TestCase


class SettingsTest(TestCase):
    def test_debug(self):
        assert settings.DEBUG == False

    def test_db(self):
        assert (
            settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql"
        )
