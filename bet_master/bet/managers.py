from django.db import models


class PendingAcceptanceBetsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_accepted=False)


class RejectedBetsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_rejected=True)


class ResolvedBetsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_resolved=True)


class PendingBetsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_accepted=True, is_rejected=False, is_resolved=False)
