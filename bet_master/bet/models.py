from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from bet_master.bet.managers import (
    PendingAcceptanceBetsManager,
    PendingBetsManager,
    RejectedBetsManager,
    ResolvedBetsManager,
)
from bet_master.users.models import User
from bet_master.utils.models import BaseModel


class Bet(BaseModel):
    """
    Model for tracking bets between users.
    """

    originator = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    odds = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    is_accepted = models.BooleanField(default=False)  # True if bet is accepted be receiver
    is_rejected = models.BooleanField(default=False)  # True if bet is rejected
    is_resolved = models.BooleanField(default=False)  # True if bet is resolved
    is_bet_deducted = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    loser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    bets = models.Manager()
    pending_acceptance_bets = PendingAcceptanceBetsManager()
    rejected_bets = RejectedBetsManager()
    pending_bets = PendingBetsManager()
    resolved_bets = ResolvedBetsManager()

    @property
    def possible_win_amount(self):
        return self.amount * self.odds

    def resolve_bet(self, winner: User):
        self.winner = winner
        self.loser = self.originator if self.winner == self.receiver else self.receiver
        if self.winner == self.originator:
            self.winner.balance += self.possible_win_amount
        else:
            self.winner.balance -= self.amount
        self.winner.save()
        self.is_resolved = True
        self.save()

    def clean(self) -> None:
        # Don't allow a winner to not be one of the bettors
        if self.winner not in [self.originator, self.receiver]:
            raise ValidationError({"winner": _("Winner must be one of the bettors.")})

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        # if the bet is accepted by the receiver, deduct the amount from the originator
        self.full_clean()
        if self.is_accepted and self.is_bet_deducted is False:
            self.originator.balance -= self.amount
            self.originator.save()
            self.receiver.balance -= self.possible_win_amount
            self.receiver.save()
            self.is_bet_deducted = True
        super().save(force_insert, force_update, *args, **kwargs)

    def __repr__(self):
        return f"{self.originator}:{self.receiver}:{self.amount}"

    def __str__(self):
        return f"{self.originator} bets {self.receiver} for ${self.amount} on {self.description}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Bet"
        verbose_name_plural = "Bets"
        default_related_name = "bet"
        default_manager_name = "bets"
