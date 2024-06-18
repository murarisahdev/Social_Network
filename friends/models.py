from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class StatusChoices(models.TextChoices):
    PENDING = "pending", _("Pending")
    ACCEPTED = "accepted", _("Accepted")
    REJECTED = "rejected", _("Rejected")

class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_friend_requests',
        verbose_name=_('From User'),
        help_text=_('User who sent the friend request')
    )
    to_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='received_friend_requests',
        verbose_name=_('To User'),
        help_text=_('User who received the friend request')
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name=_('Status')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return f"{self.from_user.first_name} to {self.to_user.first_name} - Status: {self.status}"

    class Meta:
        verbose_name = _('Friend Request')
        verbose_name_plural = _('Friend Requests')
        unique_together = ('from_user', 'to_user')
