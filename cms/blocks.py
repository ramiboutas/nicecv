from modelcluster.fields import ParentalKey

from wagtail.blocks import CharBlock
from wagtail.blocks import ChoiceBlock
from wagtail.blocks import RichTextBlock
from wagtail.blocks import StreamBlock
from wagtail.blocks import StructBlock
from wagtail.blocks import TextBlock
from wagtail.blocks import ListBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import PageChooserBlock

from wagtailsvg.blocks import SvgChooserBlock


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """

    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "cms/blocks/image.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """

    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(
        choices=[
            ("", "Select a header size"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "cms/blocks/heading.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """

    text = TextBlock()
    attribute_name = CharBlock(blank=True, required=False, label="e.g. Mary Berry")

    class Meta:
        icon = "openquote"
        template = "cms/blocks/quote.html"


class HeroSection(StructBlock):
    image = ImageChooserBlock()
    hero_type = ChoiceBlock(
        choices=[
            ("with-phone-mockup", "With phone mockup"),
            ("split-with-image", "Split with image"),
        ],
    )
    hero_title = CharBlock(
        max_length=255,
        null=True,
        help_text="Write a title",
    )
    hero_text = CharBlock(
        max_length=255,
        null=True,
        help_text="Write an introduction",
    )
    hero_cta = CharBlock(
        verbose_name="Hero CTA",
        null=True,
        max_length=255,
        help_text="Text to display on Call to Action",
    )
    hero_cta_link = PageChooserBlock()

    class Meta:
        icon = "tablet-alt"
        template = "cms/blocks/hero_section.html"


class FeatureItemBlock(StructBlock):
    name = CharBlock(
        max_length=255,
        null=True,
        blank=True,
        help_text="Feature name",
    )
    description = TextBlock(
        max_length=512,
        null=True,
        blank=True,
        help_text="Feature description",
    )
    svg = SvgChooserBlock(help_text="Feature svg")


class FeatureSection(StructBlock):
    heading_text = CharBlock(
        max_length=255,
        null=True,
        help_text="Write the heading",
    )
    slogan = CharBlock(
        max_length=255,
        null=True,
        required=False,
        help_text="Add a slogan",
    )
    description = TextBlock(
        max_length=512,
        null=True,
        required=False,
        help_text="Description of the feature section",
    )

    image = ImageChooserBlock(required=False)

    feature_type = ChoiceBlock(
        choices=[
            ("centered", "Centered"),
            ("with-offset", "With offset"),
            ("with-image-on-left", "With image on left"),
            ("with-image-on-right", "With image on right"),
        ],
    )

    items = ListBlock(
        FeatureItemBlock(),
        label="Feature items",
    )

    class Meta:
        icon = "check"
        template = "cms/blocks/feature_section.html"


# StreamBlocks
class FullStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="pilcrow",
        template="cms/blocks/paragraph.html",
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text="Insert an embed URL",
        icon="media",
        template="cms/blocks/embed.html",
    )
    hero_section = HeroSection()
    feature_section = FeatureSection()
