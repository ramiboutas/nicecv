from ..models import Setting
from config.test import TestCase


class SettingModelTests(TestCase):
    def test_setting_model(self):
        Setting.objects.create(setting_a="A", setting_b="B")

        self.assertIsNotNone(Setting.get())
