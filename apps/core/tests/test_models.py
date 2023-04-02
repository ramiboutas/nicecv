from config.test import TestCase
from ..models import Settings


class SettingModelTests(TestCase):
    def test_setting_model(self):
        Settings.objects.create(setting_a="A", setting_b="B")

        self.assertIsNotNone(Settings.get())
