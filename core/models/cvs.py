import tempfile
from functools import cache

import auto_prefetch
from pdf2image import convert_from_path
from django_tex.core import compile_template_to_pdf


from django.conf import settings
from django.db.models import Q
from django.db import models
from django.contrib.sessions.models import Session
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .profiles import Profile


def get_cv_upload_path(cv, filename):
    return f"profiles/{cv.profile.category}/{cv.profile.id}/cvs/{filename}"


class Cv(auto_prefetch.Model):
    profile = auto_prefetch.ForeignKey(Profile, on_delete=models.CASCADE)
    tex = auto_prefetch.ForeignKey("core.CvTex", null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to=get_cv_upload_path)
    pdf = models.FileField(upload_to=get_cv_upload_path)

    def render_files(self):
        bytes_pdf = compile_template_to_pdf(
            self.tex.template_name,
            {"object": self.profile.get_tex_proxy()},
        )

        self.pdf.save(f"{self.profile.id}.pdf", ContentFile(bytes_pdf), save=False)
        with tempfile.TemporaryDirectory() as temp_path:
            image = convert_from_path(
                pdf_path=self.pdf.path,
                first_page=1,
                last_page=1,
                fmt="jpg",
                output_folder=temp_path,
            )[0]
            with open(image.filename, "rb") as f:
                self.image.save(
                    f"{self.profile.id}.jpg", ContentFile(f.read()), save=False
                )

    @classmethod
    def crete_cvs_from_profile_templates(cls):
        cls.objects.filter(profile__auto_created=True).delete()
        from .tex import CvTex

        for tex in CvTex.objects.all():
            for profile in Profile.objects.filter(category="template"):
                obj = cls.objects.create(profile=profile, tex=tex)
                print(f"✅ {obj} created.")

    def save(self, *args, **kwargs):
        self.render_files()
        self.tex.add_download()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"CV ({self.profile.fullname} {self.tex})"
