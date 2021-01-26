from django.db import models
from django.utils.translation import ugettext_lazy as _

from .swot_analysis import SWOTAnalysis


class Quadrant(models.Model):
    """
    Quadrant model of the SWOTAnalysis
    """

    class QuadrandType(models.IntegerChoices):
        """
        Defines the possible types for the quadrant
        """

        STRENGTHS = 1, _("Strengths")
        WEAKNESSES = 2, _("Weaknesses")
        OPPORTUNITIES = 3, _("Opportunities")
        THREATS = 4, _("Threats")

    # Quadrant type
    q_type = models.PositiveSmallIntegerField(
        _("Quadrant type"),
        choices=QuadrandType.choices,
        null=False,
        blank=False,
    )

    # SWOT Analyse identifier (foreign key)
    analysis = models.ForeignKey(
        SWOTAnalysis,
        on_delete=models.CASCADE,
        related_name="quadrants",
    )

    class Meta:
        constraints = [
            # Ensure that each analysis does not
            # have repeated quadrants
            models.UniqueConstraint(
                fields=["q_type", "analysis"],
                name="unique_quadrant",
            ),
        ]

    def is_internal(self) -> bool:
        """
        Returns a boolean indicating if the quadrant is internal.
        A quadrant is internal if it's Strenghts or Weaknessess quadrant.
        """
        return self.q_type in [
            self.QuadrandType.STRENGTHS,
            self.QuadrandType.WEAKNESSES,
        ]

    def is_external(self) -> bool:
        """
        Returns a boolean indicating if the quadrant is external.
        A quadrant is external if it's Opportunities or Threats quadrant.
        """
        return self.q_type in [
            self.QuadrandType.OPPORTUNITIES,
            self.QuadrandType.THREATS,
        ]

    def get_total_score(self) -> float:
        """
        Calculates the sum of the score of each factor in the quadrant.
        """
        # Get all the factors associated with this
        # quadrant (reverse foreign key)
        return sum(f.get_score() for f in self.factors.all())
