from django.conf import settings
from django.test import SimpleTestCase

from utils.files import delete_file


def _create_temp_file(file_name: str, file_content: str):
    filepath = settings.TESTS_TEMP_DIR / file_name
    with open(filepath, "w+") as f:
        f.write(file_content)
    return filepath


class FilesModuleTest(SimpleTestCase):
    def test_delete_file(self):
        filepath = _create_temp_file("test_file.txt", "Hello")
        assert filepath.exists()
        assert delete_file(filepath) is None
        assert not filepath.exists()

    def test_delete_file_with_none_as_arg(self):
        assert delete_file(None) is None
