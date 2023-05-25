class ProfileChildMixin:
    def generate_html_id(self):
        return f"{self.__class__.__name__}-{self.id}"

    @property
    def _related_name(self):
        return self.__class__._meta.model_name

    @property
    def _verbose_name(self):
        return self.__class__._meta.verbose_name

    @property
    def active(self):
        return getattr(self.profile.activationsettings, self._related_name, True)

    @property
    def label(self):
        return getattr(
            self.profile.labelsettings, self._related_name, self._verbose_name
        )


class LevelMethodsMixin:
    @property
    def level_base_5_int(self):
        return (self.level * 5 / 100).__round__()

    @property
    def level_base_6_float(self):
        return self.level * 6 / 100
