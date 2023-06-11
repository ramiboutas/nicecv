from .profiles import Profile
from ..text import escape_latex


class TexProxyProfile(Profile):
    class Meta:
        proxy = True

    def get_field_value(self, field):
        return escape_latex(getattr(self, field, ""))

    def has_photo(self):
        return getattr(getattr(self, "cropped_photo"), "name") is not None

    def photo_path(self):
        if self.has_photo():
            return self.cropped_photo.path
