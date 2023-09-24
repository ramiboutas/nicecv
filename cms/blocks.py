from django.conf import settings
from wagtail.blocks import CharBlock
from wagtail.blocks import ChoiceBlock
from wagtail.blocks import ListBlock
from wagtail.blocks import PageChooserBlock
from wagtail.blocks import RichTextBlock
from wagtail.blocks import StructBlock
from wagtail.blocks import TextBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailsvg.blocks import SvgChooserBlock


class ImageSection(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """

    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "cms/blocks/image_section.html"


class HeaderSection(StructBlock):
    """
    Header Section https://tailwindui.com/components/marketing/sections/header
    """

    heading_text = CharBlock(classname="title", required=True)
    description = TextBlock(required=False)
    template_type = ChoiceBlock(
        choices=[
            ("simple", "Simple"),
            ("simple-on-dark", "Simple on dark"),
            ("centered", "Centered"),
            ("centered-on-dark", "Centered on dark"),
        ]
    )

    class Meta:
        icon = "title"
        template = "cms/blocks/header_section.html"


class QuoteSection(StructBlock):
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
    template_type = ChoiceBlock(
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

    template_type = ChoiceBlock(
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


class RichTextSection(RichTextBlock):
    class Meta:
        icon = "pilcrow"
        template = "cms/blocks/richtext.html"


class RichtTextAndImageSection(StructBlock):
    text = RichTextBlock(features=settings.CMS_RICHTEXT_FEATURES)
    image = ImageChooserBlock()

    template_type = ChoiceBlock(
        choices=[
            ("with-image-on-left", "With image on left"),
            ("with-image-on-right", "With image on right"),
        ],
    )

    class Meta:
        icon = "pilcrow"
        template = "cms/blocks/image_and_richtext.html"


class EmbedSectionBlock(EmbedBlock):
    class Meta:
        icon = "media"
        template = "cms/blocks/embed.html"
