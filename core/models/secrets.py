from django.db import models
from django.urls import reverse


class Secrets(models.Model):
    """https://github.com/shangxiao/stupid-django-tricks/tree/master/singleton_models"""

    singleton = models.BooleanField(primary_key=True, default=True)
    name = models.CharField(max_length=32, default="API keys and dynamic settings")
    # linkedin
    linkedin_client_id = models.CharField(max_length=255, blank=True)
    linkedin_client_secret = models.CharField(max_length=255, blank=True)
    linkedin_profile_id = models.CharField(max_length=255, blank=True)
    linkedin_access_token = models.CharField(max_length=255, blank=True)
    linkedin_organization_id = models.CharField(max_length=255, blank=True)
    linkedin_organization_access_token = models.CharField(max_length=255, blank=True)
    linkedin_organization_refresh_token = models.CharField(max_length=255, blank=True)

    # twitter
    twitter_username = models.CharField(max_length=255, blank=True)
    twitter_client_id = models.CharField(max_length=255, blank=True)
    twitter_client_secret = models.CharField(max_length=255, blank=True)
    twitter_api_key = models.CharField(max_length=255, blank=True)
    twitter_api_key_secret = models.CharField(max_length=255, blank=True)
    twitter_access_token = models.CharField(max_length=255, blank=True)
    twitter_access_token_secret = models.CharField(max_length=255, blank=True)
    twitter_bearer_token = models.CharField(max_length=255, blank=True)

    # facebook
    facebook_page_id = models.CharField(max_length=255, blank=True)
    facebook_page_access_token = models.CharField(max_length=255, blank=True)
    facebook_app_id = models.CharField(max_length=255, blank=True)
    facebook_app_secret_key = models.CharField(max_length=255, blank=True)

    # instagram
    instagram_page_id = models.CharField(max_length=255, blank=True)
    instagram_access_token = models.CharField(max_length=255, blank=True)

    # deepl api
    deepl_auth_key = models.CharField(max_length=255, blank=True)

    # urls (will be used in Wagtail pages)
    profiles_url = models.URLField(blank=True, null=True, editable=False)
    plans_url = models.URLField(blank=True, null=True, editable=False)
    user_dashboard_url = models.URLField(blank=True, null=True, editable=False)

    class Meta:
        constraints = (
            models.CheckConstraint(
                name="single_setting_model",
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
