
import zipfile
from io import BytesIO
from pathlib import Path

from django.conf import settings


def delete_path_file(file_path:Path=None) -> None:
    """
    This deletes a file from path (File System)
    """
    if file_path:
        file_path.unlink()


def generate_zip(files):
    """
    This generates a zip file in memory
    """
    mem_zip = BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])
    return mem_zip.getvalue()
