from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.base import File
from django.core.management.base import BaseCommand
from wagtail.models import Collection
from wagtailsvg.models import Svg


def _get_or_create_child(parent_collection, child_name):
    qs = parent_collection.get_children().filter(name=child_name)
    if qs.exists():
        return qs[0]

    return parent_collection.add_child(name=child_name)


class Command(BaseCommand):
    help = "Loads initial collections"

    def handle(self, *args, **options):
        self.stdout.write("Creating collections...")

        root = Collection.get_first_root_node()

        for path in settings.WAGTAIL_INITIAL_FILE_COLLECTIONS_DIR.iterdir():
            # svgs -> will be saved in Svg model
            if path.name == "svgs":
                self.stdout.write("Creating svgs...")
                Svg.objects.filter(title__contains="--autouploaded").delete()
                svg_root = _get_or_create_child(root, "SVGs")

                for svgdir_path in path.iterdir():
                    svg_collection = _get_or_create_child(svg_root, svgdir_path.name)
                    for svgfile_path in svgdir_path.iterdir():
                        svg_obj = Svg.objects.create(
                            collection=svg_collection,
                            title=f"{svgfile_path.name} ({svg_collection.name}) --autouploaded",
                        )
                        with open(svgfile_path) as f:
                            svg_obj.file.save(svgfile_path.name, File(f))

        self.stdout.write("Collections created.")
