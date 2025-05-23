from apps.common.models.base import BaseModel
from apps.common.utils import track_events
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _


@track_events()
class OriginalSourceClaim(BaseModel):
    REPR = "<Claim: {self.post} by {self.user}>"
    STR = "Claim on {self.post} by {self.user}"
    COMMENT_MAX_LENGTH = 1000

    class OriginalSourceClaimStatus(models.TextChoices):
        PENDING = "pending", _("Pending")
        APPROVED = "approved", _("Approved")
        REJECTED = "rejected", _("Rejected")

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="original_source_claims",
        verbose_name=_("User"),
        help_text=_("User who made the claim."),
    )
    post = models.ForeignKey(
        "core.Post",
        on_delete=models.CASCADE,
        related_name="original_source_claims",
        verbose_name=_("Post"),
        help_text=_("The post this claim is for."),
    )
    comment = models.TextField(
        verbose_name=_("Comment"),
        help_text=_("Comments about the source."),
        max_length=COMMENT_MAX_LENGTH,
    )
    source = models.URLField(
        verbose_name=_("Source"),
        help_text=_("The source of the original post."),
    )
    status = models.CharField(
        max_length=100,
        choices=OriginalSourceClaimStatus.choices,
        default=OriginalSourceClaimStatus.PENDING,
        verbose_name=_("Status"),
        help_text=_("The status of the claim."),
    )

    @transaction.atomic
    def approve(self):
        self.update(status=self.OriginalSourceClaimStatus.APPROVED)
        self.post.update(original_source=self.source)
        self.post.reposts.update(original_source=self.source)

    def reject(self):
        self.update(status=self.OriginalSourceClaimStatus.REJECTED)

    class Meta:
        verbose_name = _("Original Source Claim")
        verbose_name_plural = _("Original Source Claims")
