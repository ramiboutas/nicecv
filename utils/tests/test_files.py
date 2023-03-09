import time
from pathlib import Path
from datetime import datetime

from django.test import SimpleTestCase
from django.conf import settings

from utils.files import delete_path_file
from utils.files import generate_zip


class FilesModuleTest(SimpleTestCase):

    def test_delete_path_file(self):
        filepath = settings.BASE_DIR / "temp" / "test_file.txt"
        with open(filepath, 'w') as f:
            f.write("Hello")
        assert filepath.exists() == True
        assert delete_path_file(filepath) == None
        assert filepath.exists() == False
        # if case arg is None
        assert delete_path_file(None) == None
