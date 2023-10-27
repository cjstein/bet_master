from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

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
    is_accepted = models.BooleanField(default=False)  # True if bet is accepted be receiver
    is_resolved = models.BooleanField(default=False)  # True if bet is resolved
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def resolve_bet(self, winner: User):
        self.is_resolved = True
        self.winner = winner
        self.save()

    def clean(self) -> None:
        # Don't allow a winner to not be one of the bettors
        if self.winner not in [self.originator, self.receiver]:
            raise ValidationError({"winner": _("Winner must be one of the bettors.")})

    def __repr__(self):
        return f"{self.originator}:{self.receiver}:{self.amount}"

    def __str__(self):
        return f"{self.originator} bets {self.receiver} for ${self.amount} on {self.description}"
