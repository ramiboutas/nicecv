import tempfile
from pdf2image import convert_from_path
from django_tex.core import compile_template_to_pdf


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile

from .models import Cv


@receiver(post_save, sender=Cv)
def render_cv_files(sender, created, instance, **kwargs):
    # TODO: use in tasks!!!
    bytes_pdf = compile_template_to_pdf(
        instance.tex.template_name,
        {"object": instance.profile.get_tex_proxy()},
    )
    instance.pdf.save(f"{instance.id}.pdf", ContentFile(bytes_pdf))

    # with tempfile.TemporaryDirectory() as temp_path:
    #     image = convert_from_path(
    #         pdf_path=instance.pdf.path,
    #         first_page=1,
    #         last_page=1,
    #         fmt="jpg",
    #         output_folder=temp_path,
    #     )[0]
    #     with open(image.filename, "rb") as f:
    #         instance.image.save(f"{instance.id}.jpg", ContentFile(f.read()))
