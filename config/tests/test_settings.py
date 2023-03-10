from django.conf import settings
from django.test import override_settings
from django.test import SimpleTestCase


class SettingsTests(SimpleTestCase):
    def test_debug(self):
        assert settings.DEBUG == False

    def test_db(self):
        assert (
            settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql"
        )
