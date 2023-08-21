from django.conf import settings
from wagtail.blocks import StreamBlock

from . import blocks


# StreamBlocks
class FullStreamBlock(StreamBlock):

    """
    Define the custom blocks that `StreamField` will utilize
    """

    hero_section = blocks.HeroSection()
    header_section = blocks.HeaderSection()
    feature_section = blocks.FeatureSection()
    embed_section = blocks.EmbedSectionBlock()
    richtext_section = blocks.RichTextSection()
    richtext_and_image_section = blocks.RichtTextAndImageSection()
    quote_section = blocks.QuoteSection()
    image_section = blocks.ImageSection()


class TextStreamBlock(StreamBlock):
    rich_text_section = blocks.RichTextSection(features=settings.CMS_RICHTEXT_FEATURES)


class ArticleStreamBlock(StreamBlock):
    embed_section = blocks.EmbedSectionBlock()
    rich_text_section = blocks.RichTextSection()
    quote_section = blocks.QuoteSection()
    image_section = blocks.ImageSection()
