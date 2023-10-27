from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "bet_master.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import bet_master.users.signals  # noqa: F401
        except ImportError:
            pass
