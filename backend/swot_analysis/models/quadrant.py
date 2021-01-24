from django.db import models
from django.utils.translation import ugettext_lazy as _

from .swot_analysis import SWOTAnalysis


class Quadrant(models.Model):
    """
    Quadrant model of the SWOTAnalysis
    """

    class QuadrantName(models.TextChoices):
        """
        Defines the possible names for the quadrant
        """

        STRENGTHS = "S", _("Strengths")
        WEAKNESSES = "W", _("Weaknesses")
        OPPORTUNITIES = "O", _("Opportunities")
        THREATS = "T", _("Threats")

    # Name of the quadrant
    name = models.CharField(
        _("Quadrant name"),
        max_length=1,
        choices=QuadrantName.choices,
        blank=False,
        null=False,
    )

    # SWOT Analyse identifier (foreign key)
    analysis = models.ForeignKey(
        SWOTAnalysis,
        on_delete=models.CASCADE,
        related_name="quadrants",
    )

    class Meta:
        # Ensure that each analysis does not
        # have repeated quadrants
        constraints = [
            models.UniqueConstraint(
                fields=["name", "analysis"],
                name="unique_quadrant",
            )
        ]

    def is_internal(self) -> bool:
        """
        Returns a boolean indicating if the quadrant is internal.
        A quadrant is internal if it's Strenghts or Weaknessess quadrant.
        """
        return self.name in [
            self.QuadrantName.STRENGTHS,
            self.QuadrantName.WEAKNESSES,
        ]

    def is_external(self) -> bool:
        """
        Returns a boolean indicating if the quadrant is external.
        A quadrant is external if it's Opportunities or Threats quadrant.
        """
        return self.name in [
            self.QuadrantName.OPPORTUNITIES,
            self.QuadrantName.THREATS,
        ]

    def get_total_score(self) -> float:
        """
        Calculates the sum of the score of each factor in the quadrant.
        """
        # Get all the factors associated with this
        # quadrant (reverse foreign key)
        return sum(f.get_score() for f in self.factors.all())
