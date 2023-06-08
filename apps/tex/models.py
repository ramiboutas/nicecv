import auto_prefetch
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.utils import IntegrityError

from apps.profiles.models import Profile


def _escape_latex(s: str):
    # TODO: escape and line breaks
    # https://github.com/weinbusch/django-tex/blob/next/django_tex/filters.py
    return s


class TexProfile(Profile):
    class Meta:
        proxy = True

    def get_fullname(self):
        return _escape_latex(getattr(self, "fullname", ""))

    def has_photo(self):
        return getattr(getattr(self, "cropped_photo"), "name") is not None

    def photo_path(self):
        if self.has_photo():
            return self.cropped_photo.path


class CvTex(auto_prefetch.Model):
    title = models.CharField(max_length=64)
    template_name = models.CharField(max_length=64, unique=True)
    interpreter = models.CharField(max_length=20, default="lualatex")
    image = models.ImageField(upload_to="tex-screenshots")
    is_active = models.BooleanField(default=True)
    license = models.CharField(max_length=32)
    credits = models.CharField(max_length=128, blank=True, null=True)
    credits_url = models.URLField(max_length=128, blank=True, null=True)
    downloads = models.IntegerField(default=0)

    # name = Twenty Seconds Resume/CV
    # credits = Carmine Spagnuolo (cspagnuolo@unisa.it), Vel (vel@LaTeXTemplates.com)
    # license = MIT
    # interpreter = xelatex

    def update_metadata(self):
        pass

    @staticmethod
    def create_initial_objects():
        for path in settings.CV_TEX_DIR.iterdir():
            tex_path = path / "template.tex"
            metadata_path = path / "metadata"
            if tex_path.is_file() and metadata_path.is_file():
                CvTex.create_object_from_path(path)

    @classmethod
    def create_object_from_path(cls, path) -> dict:
        """
        Creates a new object from a path (a metadata and template.tex file are required)
        """
        tex_path = path / "template.tex"
        metadata_path = path / "metadata"
        if tex_path.is_file() and metadata_path.is_file():
            template_name = str(tex_path).replace(str(tex_path.parent.parent) + "/", "")

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

    def add_one_download(self):
        self.downloads = self.downloads + 1
        self.save()


class CoverLetterTemplate(auto_prefetch.Model):
    name = models.CharField(max_length=128)
    interpreter = models.CharField(max_length=20, default="lualatex")
    image = models.ImageField(upload_to="tex/cover-letters/screenshots")
    is_active = models.BooleanField(default=True)
    credits = models.CharField(max_length=128, blank=True, null=True)
    credits_url = models.URLField(max_length=200, blank=True, null=True)
    downloads = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def download_object_url(self):
        return reverse("tex_download_coverletter", kwargs={"pk": self.pk})
