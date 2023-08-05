from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.models import Page
from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField

from modelcluster.fields import ParentalKey

from ..streams import ArticleStreamBlock


class BlogIndexPage(Page):
    template = "cms/blog/index.html"

    parent_page_type = ["cms.HomePage"]
    subpage_types = ["cms.BlogPostPage"]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = BlogPostPage.objects.live().public().order_by("-first_published_at")
        # Paginate all posts by 24 per page
        paginator = Paginator(all_posts, 24)
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
    template = "cms/blog/post.html"
    parent_page_type = ["cms.BlogIndexPage"]
    subpage_types = ["cms.BlogPostPage"]

    description = models.TextField(max_length=1024)
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
        InlinePanel(
            "blog_person_relationship",
            heading="Authors",
            label="Author",
            panels=None,
            min_num=1,
            max_num=3,
        ),
    ]

    def authors(self):
        """
        Returns the BlogPage's related people. Again note that we are using
        the ParentalKey's related_name from the BlogPersonRelationship model
        to access these objects. This allows us to access the Person objects
        with a loop on the template. If we tried to access the blog_person_
        relationship directly we'd print `blog.BlogPersonRelationship.None`
        """
        # Only return authors that are not in draft
        return [
            n.person
            for n in self.blog_person_relationship.filter(
                person__live=True
            ).select_related("person")
        ]

    # Returns the list of Tags for all child posts of this BlogPage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags


class BlogPersonRelationship(Orderable, models.Model):
    """
    This defines the relationship between the `Person` within the `base`
    app and the BlogPage below. This allows people to be added to a BlogPage.

    We have created a two way relationship between BlogPage and Person using
    the ParentalKey and ForeignKey
    """

    page = ParentalKey(
        "cms.BlogPostPage",
        related_name="blog_person_relationship",
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        "cms.Person",
        related_name="person_blog_relationship",
        on_delete=models.CASCADE,
    )
    panels = [FieldPanel("person")]
