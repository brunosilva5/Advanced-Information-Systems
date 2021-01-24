from django.db import models
from django.utils.translation import ugettext_lazy as _
from user.models import User


class SWOTAnalysis(models.Model):

    # User associated with this analysis
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="analyses",
    )

    # Title of the analysis
    title = models.CharField(
        _("Analysis title"), max_length=200, blank=False, null=False
    )

    # Description of the analysis
    description = models.CharField(
        _("Analysis short description"), max_length=300, blank=True, null=True
    )

    # Starting date of the analysis (auto generated at creation)
    starting_date = models.DateTimeField(_("Creation date"), auto_now_add=True)

    # Define the possible states of the analysis
    class States(models.IntegerChoices):
        IN_PROGRESS = 1, _("In progress")
        CLOSED = 2, _("Closed")
        ARCHIVED = 3, _("Archived")

    state = models.IntegerField(
        choices=States.choices,
        default=States.IN_PROGRESS,
    )

    class Meta:
        verbose_name = _("SWOT analysis")
        verbose_name_plural = _("SWOT analyses")
