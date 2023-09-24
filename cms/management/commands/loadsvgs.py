from io import BytesIO

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile

from wagtail.models import Collection
from wagtail.images.models import Image

import willow


def _get_or_create_child(parent_collection, child_name):
    qs = parent_collection.get_children().filter(name=child_name)

    if qs.exists():
        return qs[0]

    return parent_collection.add_child(name=child_name)


class Command(BaseCommand):
    help = "Loads initial collections"

    def handle(self, *args, **options):
        self.stdout.write("Loading Svgs...")
        root_collection = Collection.get_first_root_node()
        images = []

        if root_collection is None:
            root_collection = Collection.add_root(name="Root")

        for path in settings.WAGTAIL_INITIAL_SVGS_DIR.iterdir():
            # svgs -> will be saved in Svg model
            collection = _get_or_create_child(root_collection, path.name)
            if Image.objects.filter(collection=collection).count() > 0:
                self.stdout.write(f"Svgs for {collection.name} already created.")
                continue
            for svgfile_path in path.iterdir():
                img_bytes = open(svgfile_path, "rb").read()
                img_file = ImageFile(BytesIO(img_bytes), name=svgfile_path.name)
                im = willow.Image.open(img_file)
                width, height = im.get_size()
                images.append(
                    Image(
                        title=svgfile_path.name,
                        file=img_file,
                        width=width,
                        height=height,
                        collection=collection,
                    )
                )
        Image.objects.bulk_create(images)

        self.stdout.write("Svgs created.")
