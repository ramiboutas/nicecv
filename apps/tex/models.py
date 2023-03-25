import auto_prefetch
from django.db import models
from django.urls import reverse


from apps.profiles.models import Profile


class TexProfile(Profile):
    # DO NOT IMPMENT THIS....
    pass

    def get_fullname(self):
        return self.fullname.text

    class Meta(Profile.Meta):
        proxy = True


class ResumeTemplate(auto_prefetch.Model):
    name = models.CharField(max_length=50)
    template_name = models.CharField(default="test.tex", max_length=20)
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
