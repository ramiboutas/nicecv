import pathlib
import tempfile
import auto_prefetch
from pdf2image import convert_from_path
from pdf2image import convert_from_bytes
from django_tex.shortcuts import render_to_pdf
from django_tex.core import compile_template_to_pdf

from django.db import models
from django.core.files.base import ContentFile
from django.core.files import File
from django.utils.functional import cached_property

from apps.profiles.models import Profile
from apps.tex.models import CvTex
from apps.core.models import Language


def get_upload_path(obj, filename):
    return f"profiles/{obj.profile.category}/{obj.profile.id}/cvs/{filename}"


class Cv(auto_prefetch.Model):
    profile = auto_prefetch.ForeignKey(Profile, on_delete=models.CASCADE)
    tex = auto_prefetch.ForeignKey(CvTex, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to=get_upload_path)
    pdf = models.FileField(upload_to=get_upload_path)

    def render_files(self):
        bytes_pdf = compile_template_to_pdf(
            self.tex.template_name,
            {"object": self.profile.get_tex_proxy()},
        )
        self.pdf.save(f"{self.id}.pdf", ContentFile(bytes_pdf))

        with tempfile.TemporaryDirectory() as temp_path:
            image = convert_from_path(
                pdf_path=self.pdf.path,
                first_page=1,
                last_page=1,
                fmt="jpg",
                output_folder=temp_path,
            )[0]
            with open(image.filename, "rb") as f:
                self.image.save(f"{self.id}.jpg", ContentFile(f.read()))

    @classmethod
    def render_profile_templates(cls):
        for tex in CvTex.objects.all():
            for profile in Profile.objects.filter(category="template"):
                obj = cls.objects.create(profile=profile, tex=tex)
                print(f"✅ {obj} created.")

    @classmethod
    def get_template_objects(cls, lang_code="en"):
        cls.objects.filter(
            profile__category="template",
            profile__language_setting__code=lang_code,
        )

    @cached_property
    def is_template(self):
        return self.profile.category == "template"

    def save(self, *args, **kwargs):
        if self.pdf is None:
            self.render_files()
        self.tex.add_download()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"CV ({self.profile.fullname} {self.tex})"
