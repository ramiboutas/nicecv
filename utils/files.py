import os
import zipfile
from io import BytesIO
from pathlib import Path

from django.conf import settings


def delete_path_file(path):
    """
    This deletes a file from path (File System)
    """
    if os.path.isfile(path):
        os.remove(path)


def get_tex_template_name(file_obj):
    """
    This get a Tex file which is used as a template (str obj) for jinja2
    """
    template_name_abs = Path(file_obj.file.path)
    template_name_rel = template_name_abs.relative_to(settings.MEDIA_ROOT)
    return str(template_name_rel)


def generate_zip(files):
    """
    This generates a zip file in memory
    """
    mem_zip = BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])
    return mem_zip.getvalue()
