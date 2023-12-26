import shutil

import auto_prefetch
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from slugger import AutoSlugField


def copy_texmf():
    shutil.rmtree(settings.DESTINATION_TEXMF_DIR, ignore_errors=False)
    shutil.copytree(
        settings.ORIGIN_TEXMF_DIR, settings.DESTINATION_TEXMF_DIR, dirs_exist_ok=True
    )
    print(f"✅ texmf copied successfully")


class Tex(auto_prefetch.Model):
    """
    tex_templates/<category>/<name>/<texfile>
    tex_templates/<category>/<name>/<metadata>
    * template_name: relative to tex_templates folder

    """

    TEX_FILENAME = "template.tex"
    METADATA_FILENAME = "metadata"

    category = models.CharField(max_length=32, editable=False)
    name = models.CharField(max_length=32, editable=False)
    template_name = models.CharField(max_length=64, unique=True, editable=False)
    title = models.CharField(max_length=64, editable=False)
    interpreter = models.CharField(max_length=32, default="xelatex", editable=False)
    interpreter_options = models.CharField(max_length=64, default="", editable=False)
    license = models.CharField(max_length=64, default="MIT", editable=False)
    credits = models.CharField(max_length=128, null=True, editable=False)
    source_url = models.URLField(max_length=255, null=True, editable=False)
    downloads = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    @cached_property
    def average_rendering_time(self):
        qs = self.cv_set.all()
        total_cvs = qs.count()
        total_time = qs.aggregate(Sum("rendering_time"))["rendering_time__sum"]
        return total_time / total_cvs if total_cvs > 0 else 0

    @classmethod
    def update_objects(cls):
        # tex_templates/<category>/<name>/<texfile>
        for category_path in settings.TEX_TEMPLATES_DIR.iterdir():
            for path in category_path.iterdir():
                tex_path = path / Tex.TEX_FILENAME
                metadata_path = path / Tex.METADATA_FILENAME
                if tex_path.is_file() and metadata_path.is_file():
                    template_name = (
                        f"{category_path.name}/{path.name}/{Tex.TEX_FILENAME}"
                    )
                    obj, _ = cls.objects.get_or_create(template_name=template_name)
                    obj.update_object()

    def _get_metadata_path(self):
        return (
            settings.TEX_TEMPLATES_DIR
            / self.category
            / self.name
            / Tex.METADATA_FILENAME
        )

    def update_object(self):
        self.category = self.template_name.split("/")[0]
        self.name = self.template_name.split("/")[1]

        # reading metadata file
        with open(self._get_metadata_path()) as f:
            data = f.read()
        lines = data.split("\n")
        attrs = {
            line.split(" = ")[0].strip(): line.split(" = ")[1].strip()
            for line in lines
            if " = " in line
        }

        string_attrs = ("title", "interpreter", "license", "credits", "source")
        bool_attrs = ()  #  ("is_premium",)

        try:
            for key, value in attrs.items():
                if key in string_attrs:
                    setattr(self, key, value)
                elif key in bool_attrs:
                    setattr(self, key, bool(int(value)))
            self.save()
        except Exception as e:
            e.add_note(f"🔴 The was an error with {self.template_name}")
            raise

    def __str__(self):
        return f"Tex ({self.title})"

    def add_download(self):
        self.downloads = self.downloads + 1
        self.save()
