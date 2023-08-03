from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from modelcluster.fields import ParentalKey

from taggit.models import Tag, TaggedItemBase


from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index


from wagtail.models import Page

from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from ..streams import ArticleStreamBlock


class BlogPageTag(TaggedItemBase):
    """
    This model allows us to create a many-to-many relationship between
    the BlogPage object and tags. There's a longer guide on using it at
    https://docs.wagtail.org/en/stable/reference/pages/model_recipes.html#tagging
    """

    content_object = ParentalKey("cms.BlogPostPage", related_name="tagged_items")


class BlogIndexPage(Page):
    template = "cms/blog_index.html"

    parent_page_type = ["cms.HomePage"]
    subpage_types = ["cms.BlogPostPage"]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = BlogPostPage.objects.live().public().order_by("-first_published_at")
        # Paginate all posts by 2 per page
        paginator = Paginator(all_posts, 2)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["posts"] = posts
        return context

    def get_posts(self, tag=None):
        posts = BlogPostPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts


class BlogPostPage(Page):
    template = "cms/blog_post.html"
    parent_page_type = ["cms.BlogIndexPage"]
    subpage_types = ["cms.BlogPostPage"]

    description = models.TextField(
        max_length=1024,
        null=True,
        blank=True,
    )
    body = StreamField(
        ArticleStreamBlock(),
        null=True,
        blank=True,
        use_json_field=True,
        collapsed=False,
    )
    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("body"),
    ]

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    # Returns the list of Tags for all child posts of this BlogPage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags
