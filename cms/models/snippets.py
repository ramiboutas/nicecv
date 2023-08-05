from django.db import models

from wagtail.snippets.models import register_snippet
from ..utils import localized_fieldpanel_list

from wagtail.admin.panels import FieldPanel


@register_snippet
class FrequentAskedQuestion(models.Model):
    FAQ_CHOICES = (
        ("pricing", "Related to Pricing"),
        ("featured", "Featured"),
    )
    question = models.CharField(max_length=128)
    answer = models.TextField()
    category = models.CharField(max_length=16, choices=FAQ_CHOICES)
    active = models.BooleanField(default=True)

    panels = (
        [
            FieldPanel("active"),
            FieldPanel("category"),
        ]
        + localized_fieldpanel_list("question")
        + localized_fieldpanel_list("answer")
    )

    def __str__(self) -> str:
        return self.question


from django.db import models
from django.utils.translation import gettext as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PublishingPanel,
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import (
    Collection,
    DraftStateMixin,
    LockableMixin,
    Page,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
    WorkflowMixin,
)
from wagtail.search import index


@register_snippet
class Person(
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    PreviewableMixin,
    index.Indexed,
    ClusterableModel,
):
    """
    A Django model to store Person objects.
    It is registered using `register_snippet` as a function in wagtail_hooks.py
    to allow it to have a menu item within a custom menu item group.

    `Person` uses the `ClusterableModel`, which allows the relationship with
    another model to be stored locally to the 'parent' model (e.g. a PageModel)
    until the parent is explicitly saved. This allows the editor to use the
    'Preview' button, to preview the content, without saving the relationships
    to the database.
    https://github.com/wagtail/django-modelcluster
    """

    name = models.CharField("Full name", max_length=256)
    job_title = models.CharField("Job title", max_length=254)

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("job_title"),
        FieldPanel("image"),
        PublishingPanel(),
    ]

    search_fields = [
        index.SearchField("name"),
        index.FilterField("job_title"),
        index.AutocompleteField("name"),
    ]

    @property
    def thumb_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.image.get_rendition("fill-50x50").img_tag()
        except:  # noqa: E722 FIXME: remove bare 'except:'
            return ""

    @property
    def preview_modes(self):
        return PreviewableMixin.DEFAULT_PREVIEW_MODES + [("blog_post", _("Blog post"))]

    def __str__(self):
        return self.name

    def get_preview_template(self, request, mode_name):
        from cms.models.blog import BlogPostPage

        if mode_name == "blog_post":
            return BlogPostPage.template
        return "cms/preview/person.html"

    def get_preview_context(self, request, mode_name):
        from cms.models.blog import BlogPostPage

        context = super().get_preview_context(request, mode_name)
        if mode_name == self.default_preview_mode:
            return context

        page = BlogPostPage.objects.filter(
            blog_person_relationship__person=self
        ).first()
        if page:
            # Use the page authored by this person if available,
            # and replace the instance from the database with the edited instance
            page.authors = [
                self if author.pk == self.pk else author for author in page.authors()
            ]
            # The authors() method only shows live authors, so make sure the instance
            # is included even if it's not live as this is just a preview
            if not self.live:
                page.authors.append(self)
        else:
            # Otherwise, get the first page and simulate the person as the author
            page = BlogPostPage.objects.first()
            page.authors = [self]

        context["page"] = page
        return context

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
