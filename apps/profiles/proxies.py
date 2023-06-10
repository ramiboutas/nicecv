from apps.profiles.models import Profile
from apps.core.text import escape_latex


class TexProxyProfile(Profile):
    class Meta:
        proxy = True

    def get_fullname(self):
        return escape_latex(getattr(self, "fullname", ""))

    def has_photo(self):
        return getattr(getattr(self, "cropped_photo"), "name") is not None

    def photo_path(self):
        if self.has_photo():
            return self.cropped_photo.path
