import auto_prefetch
from django.db import models
from django.urls import reverse

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
    name = models.CharField(max_length=50)
    template_name = models.CharField(default="test.tex", max_length=20, unique=True)
    only_one_page_allowed = models.BooleanField(default=False)
    interpreter = models.CharField(max_length=20, default="lualatex")
    image = models.ImageField(upload_to="tex-screenshots")
    is_active = models.BooleanField(default=True)
    credits = models.CharField(max_length=50, blank=True, null=True)
    credits_url = models.URLField(max_length=100, blank=True, null=True)
    downloads = models.IntegerField(default=0)

    def __str__(self):
        return self.name

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
