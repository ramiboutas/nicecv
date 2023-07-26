# Generated by Django 4.2.2 on 2023-07-26 20:25

from django.db import migrations
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtailsvg.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0030_alter_homepage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "heading_block",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading_text",
                                    wagtail.blocks.CharBlock(
                                        form_classname="title", required=True
                                    ),
                                ),
                                (
                                    "size",
                                    wagtail.blocks.ChoiceBlock(
                                        blank=True,
                                        choices=[
                                            ("", "Select a header size"),
                                            ("h2", "H2"),
                                            ("h3", "H3"),
                                            ("h4", "H4"),
                                        ],
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "paragraph_block",
                        wagtail.blocks.RichTextBlock(
                            icon="pilcrow", template="cms/blocks/paragraph.html"
                        ),
                    ),
                    (
                        "image_block",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=True
                                    ),
                                ),
                                ("caption", wagtail.blocks.CharBlock(required=False)),
                                (
                                    "attribution",
                                    wagtail.blocks.CharBlock(required=False),
                                ),
                            ]
                        ),
                    ),
                    (
                        "block_quote",
                        wagtail.blocks.StructBlock(
                            [
                                ("text", wagtail.blocks.TextBlock()),
                                (
                                    "attribute_name",
                                    wagtail.blocks.CharBlock(
                                        blank=True,
                                        label="e.g. Mary Berry",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "embed_block",
                        wagtail.embeds.blocks.EmbedBlock(
                            help_text="Insert an embed URL",
                            icon="media",
                            template="cms/blocks/embed.html",
                        ),
                    ),
                    (
                        "hero_section",
                        wagtail.blocks.StructBlock(
                            [
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    "hero_type",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("with-phone-mockup", "With phone mockup"),
                                            ("split-with-image", "Split with image"),
                                        ]
                                    ),
                                ),
                                (
                                    "hero_title",
                                    wagtail.blocks.CharBlock(
                                        help_text="Write a title",
                                        max_length=255,
                                        null=True,
                                    ),
                                ),
                                (
                                    "hero_text",
                                    wagtail.blocks.CharBlock(
                                        help_text="Write an introduction",
                                        max_length=255,
                                        null=True,
                                    ),
                                ),
                                (
                                    "hero_cta",
                                    wagtail.blocks.CharBlock(
                                        help_text="Text to display on Call to Action",
                                        max_length=255,
                                        null=True,
                                        verbose_name="Hero CTA",
                                    ),
                                ),
                                ("hero_cta_link", wagtail.blocks.PageChooserBlock()),
                            ]
                        ),
                    ),
                    (
                        "feature_section",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "heading_text",
                                    wagtail.blocks.CharBlock(
                                        help_text="Write the heading",
                                        max_length=255,
                                        null=True,
                                    ),
                                ),
                                (
                                    "slogan",
                                    wagtail.blocks.CharBlock(
                                        help_text="Add a slogan",
                                        max_length=255,
                                        null=True,
                                        required=False,
                                    ),
                                ),
                                (
                                    "description",
                                    wagtail.blocks.TextBlock(
                                        help_text="Description of the feature section",
                                        max_length=512,
                                        null=True,
                                        required=False,
                                    ),
                                ),
                                (
                                    "image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=False
                                    ),
                                ),
                                (
                                    "feature_type",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("centered", "Centered"),
                                            ("with-offset", "With offset"),
                                            (
                                                "with-image-on-left",
                                                "With image on left",
                                            ),
                                            (
                                                "with-image-on-right",
                                                "With image on right",
                                            ),
                                        ]
                                    ),
                                ),
                                (
                                    "items",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "name",
                                                    wagtail.blocks.CharBlock(
                                                        blank=True,
                                                        help_text="Feature name",
                                                        max_length=255,
                                                        null=True,
                                                    ),
                                                ),
                                                (
                                                    "description",
                                                    wagtail.blocks.TextBlock(
                                                        blank=True,
                                                        help_text="Feature description",
                                                        max_length=512,
                                                        null=True,
                                                    ),
                                                ),
                                                (
                                                    "svg",
                                                    wagtailsvg.blocks.SvgChooserBlock(
                                                        help_text="Feature svg"
                                                    ),
                                                ),
                                            ]
                                        ),
                                        label="Feature items",
                                    ),
                                ),
                            ]
                        ),
                    ),
                ],
                blank=True,
                null=True,
                use_json_field=True,
                verbose_name="Home content block",
            ),
        ),
    ]
