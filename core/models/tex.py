import auto_prefetch
from slugger import AutoSlugField

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.utils import IntegrityError


class CvTex(auto_prefetch.Model):
    title = models.CharField(max_length=64)
    slug = AutoSlugField(populate_from="title")
    template_name = models.CharField(max_length=64, unique=True)
    interpreter = models.CharField(max_length=20, default="lualatex")
    image = models.ImageField(upload_to="tex-screenshots")
    is_active = models.BooleanField(default=True)
    license = models.CharField(max_length=32)
    credits = models.CharField(max_length=128, blank=True, null=True)
    credits_url = models.URLField(max_length=128, blank=True, null=True)
    downloads = models.IntegerField(default=0)

    def update_metadata(self):
        pass

    @classmethod
    def update_objects(cls):
        # first remove the previous ones
        cls.objects.all().delete()
        # then read the cv tex path and save them
        for path in settings.CV_TEX_DIR.iterdir():
            tex_path = path / "template.tex"
            metadata_path = path / "metadata"
            if tex_path.is_file() and metadata_path.is_file():
                cls.create_object_from_path(path)

    @classmethod
    def create_object_from_path(cls, path) -> dict:
        """
        Creates a new object from a path (a metadata and template.tex file are required)
        """
        tex_path = path / "template.tex"
        metadata_path = path / "metadata"
        if tex_path.is_file() and metadata_path.is_file():
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
            cls.objects.create(template_name=template_name, **attrs)
            print(f"✅ {template_name} created")
        except IntegrityError:
            print(f"⚠️  {template_name} was already created")
        except TypeError as e:
            print(f"🔴 {template_name} had an error: {e}")

    def __str__(self):
        return self.title

    def download_object_url(self):
        return reverse("tex_download_resume", kwargs={"pk": self.pk})

    def add_download(self):
        self.downloads = self.downloads + 1
        self.save()
