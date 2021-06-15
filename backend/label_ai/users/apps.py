from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "label_ai.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import label_ai.users.signals  # noqa F401
        except ImportError:
            pass
