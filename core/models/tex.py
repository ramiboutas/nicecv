import auto_prefetch
from slugger import AutoSlugField

from django.db import models
from django.urls import reverse
from django.conf import settings

from .params import *


class CvTex(auto_prefetch.Model):
    title = models.CharField(max_length=64)
    slug = AutoSlugField(populate_from="title")
    template_name = models.CharField(max_length=64, unique=True)
    interpreter = models.CharField(max_length=32, default="lualatex")
    license = models.CharField(max_length=32)
    credits = models.CharField(**null_blank_128)
    credits_url = models.URLField(**null_blank_128)
    downloads = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def update_metadata(self):
        pass

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

        with open(metadata_path, "r") as f:
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
            print(f"🔴 The was an error with {obj}: {e}")

    def __str__(self):
        return self.title

    def download_object_url(self):
        return reverse("tex_download_resume", kwargs={"pk": self.pk})

    def add_download(self):
        self.downloads = self.downloads + 1
        self.save()
