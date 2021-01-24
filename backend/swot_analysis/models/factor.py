"""
Defines the Factor Model
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from .quadrant import Quadrant


class Factor(models.Model):
    """
    Factor model of the SWOT Analysis
    """

    # Possible factor classification
    class FactorClassification(models.IntegerChoices):
        """
        Defines the possible choices for the classification of the factor
        """

        STRENGTH = 0, _("Strength")
        WEAKNESS = 1, _("Weakness")
        THREAT = 2, _("Threat")
        OPPORTUNITY = 4, _("Opportunity")

    # Possible types of importance.
    # Designed according to:
    # https://researchbasics.education.uconn.edu/likert_scales/#
    class FactorImportance(models.IntegerChoices):
        """
        Defines the possible choices for the importance of the factor
        """

        UNIMPORTANT = 0, _("Unimportant")
        OF_LITTLE_IMPORTANCE = 1, _("Of Little Importance")
        MODERATELY_IMPORTANT = 2, _("Moderately Important ")
        IMPORTANT = 3, _("Important")
        VERY_IMPORTANT = 4, _("Very Important")

    # Quadrant associated with this factor
    quadrant = models.ForeignKey(
        Quadrant,
        on_delete=models.CASCADE,
        related_name="factors",
    )

    # Classification of the factor
    classification = models.PositiveSmallIntegerField(
        _("Factor classification"),
        choices=FactorClassification.choices,
        null=False,
        blank=False,
    )

    # Description of the factor. Maximum caracters should be 50
    # (Consult requirements -  RNF1/RNF2)
    description = models.CharField(
        _("Factor description"), max_length=50, null=False, blank=False
    )

    # Importance of the factor
    importance = models.IntegerField(
        _("Factor importance"),
        choices=FactorImportance.choices,
        null=False,
        blank=False,
    )

    # Override clean method to validate fields
    def clean(self) -> None:
        # An internal factor can only have one of the
        # following classifications: ["Strength", "Weakness"]
        if self.quadrant.is_internal():
            allowed = [
                self.FactorClassification.STRENGTH,
                self.FactorClassification.WEAKNESS,
            ]
            if self.classification not in allowed:
                raise ValidationError(
                    _(
                        "An internal factor can only have the following classifications: %(value)s",  # noqa
                    ),
                    code="invalid",
                    params={"value": allowed},
                )

        elif self.quadrant.is_external():
            # An external factor can only have one of the
            # following classifications: ["Threat", "Opportunity"]
            allowed = [
                self.FactorClassification.THREAT,
                self.FactorClassification.OPPORTUNITY,
            ]
            if self.classification not in allowed:
                raise ValidationError(
                    _(
                        "An external factor can only have the following classifications: %(value)s",  # noqa
                    ),
                    code="invalid",
                    params={"value": allowed},
                )

        super(Factor, self).clean()

    # Ovveride save method to perform full-cleaning on the model
    def save(self, *args, **kwargs):
        # Call `full_clean` (which calls `clean`)
        self.full_clean()
        super(Factor, self).save(*args, **kwargs)

    def get_score(self) -> float:
        """
        Calculates the score of the factor. The score is based
        on factor importance.
        It basically translates textual importance into a numerical value.
        """
        # We multiply current importance by 2.5
        return self.importance * 2.5
