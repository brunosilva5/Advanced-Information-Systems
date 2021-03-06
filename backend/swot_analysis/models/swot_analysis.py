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
    class SWOTAnalysisStates(models.IntegerChoices):
        OPEN = 1, _("Open")
        CLOSED = 2, _("Closed")

    state = models.IntegerField(
        choices=SWOTAnalysisStates.choices,
        default=SWOTAnalysisStates.OPEN,
    )

    class Meta:
        verbose_name = _("SWOT analysis")
        verbose_name_plural = _("SWOT analyses")
        # Make each user have unique analyses titles
        # For more info consult requirements - RFN7
        constraints = [
            # Ensure that each analysis does not
            # have repeated quadrants
            models.UniqueConstraint(
                fields=["user", "title"],
                name="unique_analysis",
            ),
        ]
