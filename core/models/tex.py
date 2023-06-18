import shutil

import auto_prefetch

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from slugger import AutoSlugField


def copy_latex_local_files_to_destination():
    dest = settings.DESTINATION_LATEX_LOCAL_DIR
    for path in settings.ORIGIN_LATEX_LOCAL_DIR.iterdir():
        if path.is_dir() and not path.is_file():
            continue
        shutil.copy(path, dest / path.name)
        print(f"✅ {path.name} copied to {dest}")


class CvTex(auto_prefetch.Model):
    title = models.CharField(
        max_length=64,
        editable=False,
        help_text=_("Read from metadata"),
    )
    slug = AutoSlugField(
        populate_from="title",
        editable=False,
        help_text=_("Calculated from title field"),
    )
    template_name = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
        help_text=_("Read from metadata"),
    )
    interpreter = models.CharField(
        max_length=32,
        default="lualatex",
        editable=False,
        help_text=_("Read from metadata"),
    )
    license = models.CharField(
        max_length=32,
        default="MIT",
        editable=False,
        help_text=_("Read from metadata"),
    )
    credits = models.CharField(
        max_length=128,
        null=True,
        editable=False,
        help_text=_("Read from metadata"),
    )
    credits_url = models.URLField(
        max_length=128,
        null=True,
        editable=False,
        help_text=_("Read from metadata"),
    )
    downloads = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    @cached_property
    def average_rendering_time(self):
        qs = self.cv_set.all()
        total_cvs = qs.count()
        total_time = qs.aggregate(Sum("rendering_time"))["rendering_time__sum"]
        return total_time / total_cvs if total_cvs > 0 else 0

    @classmethod
    def update_objects(cls):
        for path in settings.CV_TEX_DIR.iterdir():
            tex_path, metadata_path = path / "template.tex", path / "metadata"
            if tex_path.is_file() and metadata_path.is_file():
                cls.update_object(tex_path, metadata_path)

    @classmethod
    def update_object(cls, tex_path, metadata_path):
        """
        Updates an object from a path (metadata and template.tex files are required)
        """

        template_name = str(tex_path).replace(
            str(tex_path.parent.parent.parent) + "/", ""
        )

        with open(metadata_path) as f:
            data = f.read()
        lines = data.split("\n")
        attrs = {
            line.split(" = ")[0].strip(): line.split(" = ")[1].strip()
            for line in lines
            if " = " in line
        }

        try:
            obj, _ = cls.objects.get_or_create(template_name=template_name)
            for key, value in attrs.items():
                setattr(obj, key, value)
                obj.save()
            print(f"✅ {obj} created")
        except Exception as e:
            print(f"🔴 The was an error with {template_name}: {e}")

    def __str__(self):
        return self.title

    def download_object_url(self):
        return reverse("tex_download_resume", kwargs={"pk": self.pk})

    def add_download(self):
        self.downloads = self.downloads + 1
        self.save()
