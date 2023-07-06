# Generated by Django 4.2.2 on 2023-07-06 06:59

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtailmenus.models.menuitems
import wagtailmenus.models.menus
import wagtailmenus.models.mixins


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
        ("cms", "0010_delete_rootpage"),
    ]

    operations = [
        migrations.CreateModel(
            name="LocalizedMainMenu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "max_levels",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "1: No sub-navigation (flat)"),
                            (2, "2: Allow 1 level of sub-navigation"),
                            (3, "3: Allow 2 levels of sub-navigation"),
                            (4, "4: Allow 3 levels of sub-navigation"),
                        ],
                        default=2,
                        help_text="The maximum number of levels to display when rendering this menu. The value can be overidden by supplying a different <code>max_levels</code> value to the <code>{% main_menu %}</code> tag in your templates.",
                        verbose_name="maximum levels",
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.site",
                        verbose_name="site",
                    ),
                ),
            ],
            options={
                "verbose_name": "main menu",
                "verbose_name_plural": "main menu",
                "abstract": False,
            },
            bases=(
                wagtailmenus.models.mixins.DefinesSubMenuTemplatesMixin,
                models.Model,
                wagtailmenus.models.menus.Menu,
            ),
        ),
        migrations.CreateModel(
            name="LocalizedMainMenuItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "link_url",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="link to a custom URL",
                    ),
                ),
                (
                    "url_append",
                    models.CharField(
                        blank=True,
                        help_text="Use this to optionally append a #hash or querystring to the above page's URL.",
                        max_length=255,
                        verbose_name="append to URL",
                    ),
                ),
                (
                    "handle",
                    models.CharField(
                        blank=True,
                        help_text="Use this field to optionally specify an additional value for each menu item, which you can then reference in custom menu templates.",
                        max_length=100,
                        verbose_name="handle",
                    ),
                ),
                (
                    "link_text",
                    models.CharField(
                        blank=True,
                        help_text="Provide the text to use for a custom URL, or set on an internal page link to use instead of the page's title.",
                        max_length=255,
                        verbose_name="link text",
                    ),
                ),
                (
                    "allow_subnav",
                    models.BooleanField(
                        default=True,
                        help_text="NOTE: The sub-menu might not be displayed, even if checked. It depends on how the menu is used in this project's templates.",
                        verbose_name="allow sub-menu for this item",
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.page",
                        verbose_name="link to an internal page",
                    ),
                ),
                (
                    "menu",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="menu_items",
                        to="cms.localizedmainmenu",
                    ),
                ),
            ],
            options={
                "verbose_name": "menu item",
                "verbose_name_plural": "menu items",
                "ordering": ("sort_order",),
                "abstract": False,
            },
            bases=(models.Model, wagtailmenus.models.menuitems.MenuItem),
        ),
    ]
