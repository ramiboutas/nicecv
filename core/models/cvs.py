import time
import tempfile
from pathlib import Path
from functools import cache
from subprocess import PIPE, run, CalledProcessError

import auto_prefetch
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.template.loader import get_template

from ..exceptions import TexError
from pdf2image import convert_from_path

from .profiles import Profile

# from ..tex.compile import compile_template_to_pdf


def get_cv_upload_path(cv, filename):
    return f"profiles/{cv.profile.category}/{cv.profile.id}/cvs/{filename}"


class Cv(auto_prefetch.Model):
    profile = auto_prefetch.ForeignKey("core.Profile", on_delete=models.CASCADE)
    tex = auto_prefetch.ForeignKey("core.Tex", null=True, on_delete=models.SET_NULL)
    rendered_text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=get_cv_upload_path)
    pdf = models.FileField(upload_to=get_cv_upload_path)
    pdf_time = models.FloatField(default=0)
    image_time = models.FloatField(default=0)
    rendering_time = models.FloatField(default=0)
    auto_created = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def render_files(self):
        pdf_start = time.time()
        # rendering pdf file
        template = get_template(self.tex.template_name, using="tex")
        self.rendered_text = template.render({"profile": self.profile})
        with tempfile.TemporaryDirectory() as tempdir:
            temppath = Path(tempdir)
            filename = "texput.tex"
            with open(temppath / filename, "x", encoding="utf-8") as f:
                f.write(self.rendered_text)
            args = f"{self.tex.interpreter} -interaction=batchmode {self.tex.interpreter_options} {filename} 2>&1 > /dev/null"
            try:
                run(args, shell=True, stdout=PIPE, stderr=PIPE, check=True, cwd=tempdir)
            except CalledProcessError as called_process_error:
                try:
                    with open(temppath / "texput.log", "r", encoding="utf-8") as f:
                        log = f.read()
                except FileNotFoundError:
                    raise called_process_error
                else:
                    raise TexError(
                        log=log,
                        source=self.rendered_text,
                        template_name=self.tex.template_name,
                    )
            with open(temppath / "texput.pdf", "rb") as f:
                bytes_pdf = f.read()

            self.pdf.save(f"{self.profile.id}.pdf", ContentFile(bytes_pdf), save=False)
            # pdf time calculations
            pdf_end = time.time()
            self.pdf_time = pdf_end - pdf_start
            # create the image  file
            image = convert_from_path(
                pdf_path=temppath / "texput.pdf",
                first_page=1,
                last_page=1,
                fmt="jpg",
                output_folder=temppath,
            )[0]
            with open(image.filename, "rb") as f:
                self.image.save(
                    f"{self.profile.id}.jpg",
                    ContentFile(f.read()),
                    save=False,
                )
            # total and image time calculations
            self.image_time = time.time() - pdf_end
            self.rendering_time = self.image_time + self.pdf_time

    @classmethod
    def crete_cvs_from_profile_templates(cls):
        cls.objects.filter(profile__auto_created=True).delete()
        from .tex import Tex

        for tex in Tex.objects.all():
            for profile in Profile.objects.filter(category="template"):
                obj = cls.objects.create(profile=profile, tex=tex, auto_created=True)
                print(f"✅ {obj} created.")

    def save(self, *args, **kwargs):
        self.render_files()
        self.tex.add_download()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"CV ({self.profile.fullname} {self.tex})"

    class Meta(auto_prefetch.Model.Meta):
        ordering = ["-created"]
