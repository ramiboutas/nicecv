import pathlib

import auto_prefetch
from pdf2image import convert_from_path

from django.db import models
from django.core.files.base import ContentFile
from django.utils.functional import cached_property
from apps.profiles.models import Profile
from apps.tex.models import CvTex
from apps.core.models import Language

from django_tex.shortcuts import render_to_pdf
from django_tex.core import compile_template_to_pdf


def get_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "profiles/{0}/cvs/{1}".format(instance.profile.id, filename)


class Cv(auto_prefetch.Model):
    profile = auto_prefetch.ForeignKey(Profile, on_delete=models.CASCADE)
    tex = auto_prefetch.ForeignKey(CvTex, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to=get_upload_path)
    pdf = models.FileField(upload_to=get_upload_path)

    def render_files(self):
        tex_profile = self.profile.get_tex_proxy()
        bytes_pdf = compile_template_to_pdf(
            self.tex.template_name, {"object": tex_profile}
        )

        self.pdf.save(f"{self.id}.pdf", ContentFile(bytes_pdf))
        # TODO: create image
        image = convert_from_path(
            pdf_path=self.pdf.path,
            first_page=1,
            last_page=1,
            output_folder=pathlib.Path(self.pdf.path).parent,
        )[0]

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
