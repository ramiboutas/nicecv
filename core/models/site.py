from django.db import models
from django.urls import reverse


class SiteUrls(models.Model):
    """https://github.com/shangxiao/stupid-django-tricks/tree/master/singleton_models"""

    singleton = models.BooleanField(primary_key=True, default=True)

    # urls (will be used in Wagtail pages)
    profiles_url = models.URLField(blank=True, null=True, editable=False)
    plans_url = models.URLField(blank=True, null=True, editable=False)
    user_dashboard_url = models.URLField(blank=True, null=True, editable=False)

    class Meta:
        constraints = (
            models.CheckConstraint(
                name="single_siteurls_model",
                check=models.Q(singleton=True),
            ),
        )

    @classmethod
    def get(cls):
        return cls.objects.get_or_create(singleton=True)[0]

    def update_urls(self):
        self.profiles_url = reverse("profiles:list")
        self.plans_url = reverse("plans:list")
        self.user_dashboard_url = reverse("users:dashboard")

    def save(self, *args, **kwargs):
        self.update_urls()
        super().save(*args, **kwargs)
