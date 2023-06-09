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


class Cv(auto_prefetch.Model):
    profile = auto_prefetch.ForeignKey(Profile, on_delete=models.CASCADE)
    tex = auto_prefetch.OneToOneField(CvTex, null=True, on_delete=models.SET_NULL)
    language = auto_prefetch.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
    is_template = models.BooleanField(default=False)
    lang_code = models.CharField(max_length=5, default="en")
    image = models.ImageField()
    pdf = models.FileField()

    def render_files(self):
        tex_profile = self.profile.get_tex_proxy()
        bytes_pdf = compile_template_to_pdf(
            self.tex.template_name, {"object": tex_profile}
        )
        self.pdf = ContentFile(bytes_pdf, f"{self.id}.pdf")
        self.pdf.save()
        # TODO: create image
        image = convert_from_path(
            pdf_path=self.pdf.path,
            first_page=1,
            last_page=1,
            output_folder=self.pdf.path.parent,
        )[0]

    @classmethod
    def render_profile_templates(cls):
        for tex_obj in CvTex.objects.all():
            cvs = []
            for profile in Profile.objects.filter(category="template"):
                cvs.append(cls(tex_profile=profile, tex=tex_obj))
            cls.objects.bulk_create(cvs)

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
        super(Cv, self).save(self, *args, **kwargs)
