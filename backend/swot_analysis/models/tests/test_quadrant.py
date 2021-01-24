from swot_analysis.models.factor import Factor
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
import string
from django.db import transaction

from ..quadrant import Quadrant
from ..swot_analysis import SWOTAnalysis

from user.models import User


class QuadrantTestCase(TestCase):
    """
    Quadrant model related tests
    """

    def setUp(self) -> None:
        # First create a user
        user = User(first_name="John", last_name="Test", email="john@email.pt")
        user.save()
        # Create an analysis for this user
        analysis = SWOTAnalysis(title="Sample", user=user)
        analysis.save()
        self.analysis = analysis
        return super().setUp()

    def test_quadrant_invalid_name_choice(self):
        """
        Tests the quadrant name choices
        """
        # Create a list with all ascii chars
        all_choices = list(string.printable)
        # Create a list with valid choices
        valid_choices = ["S", "W", "O", "T"]

        # Iterate over all possible choices
        for c in all_choices:
            # If `c` not a valid choice
            # ensure that a exception is raised
            if c not in valid_choices:
                with self.assertRaises(ValidationError) as exc:
                    quadrant = Quadrant(name="a" * 2)
                    quadrant.full_clean()

                exception = exc.exception
                self.assertIn("name", exception.error_dict)
                name_exceptions = exception.error_dict["name"]
                self.assertEqual(1, len(name_exceptions))
                name_exception = name_exceptions[0]
                self.assertEqual("invalid_choice", name_exception.code)

    def test_no_duplicate_quadrants(self):
        """
        Tests that a analysis can't have duplicate quadrants.
        Check: https://stackoverflow.com/questions/21458387/transactionmanagementerror-you-cant-execute-queries-until-the-end-of-the-atom
        """  # noqa

        valid_choices = ["S", "W", "O", "T"]

        for c in valid_choices:
            # Create quadrant
            Quadrant.objects.create(name=c, analysis=self.analysis)
            try:
                with transaction.atomic():
                    # Duplicates should be prevented.
                    Quadrant.objects.create(name=c, analysis=self.analysis)
                self.fail("Duplicate quadrants should not be allowed.")
            except IntegrityError:
                pass

    def test_internal_external_quadrants(self):
        """
        Tests if a quadrant is correctly classified as internal/external
        """
        internal_names = ["S", "W"]
        external_names = ["O", "T"]

        for name in internal_names:
            quadrant = Quadrant.objects.create(
                name=name,
                analysis=self.analysis,
            )
            self.assertTrue(
                quadrant.is_internal(),
                "Quadrant call to `is_internal` did not correctly classify as internal",  # noqa
            )

        for name in external_names:
            quadrant = Quadrant.objects.create(
                name=name,
                analysis=self.analysis,
            )
            self.assertTrue(
                quadrant.is_external(),
                "Quadrant call to `is_external` did not correctly classify as internal",  # noqa
            )

    def test_total_score(self):
        """
        Tests if a quadrant is correctly calculating total score
        """
        # Create a quadrant
        quadrant = Quadrant.objects.create(
            name=Quadrant.QuadrantName.STRENGTHS,
            analysis=self.analysis,
        )

        # Create factors for this quadrant
        factor_importance_tupples = Factor.FactorImportance.choices
        # `factor_importance_tupples` return a list of tuples (int, str)
        factor_importances = [el[0] for el in factor_importance_tupples]

        for imp in factor_importances:
            factor = Factor(
                quadrant=quadrant,
                description="Test",
                classification=Factor.FactorClassification.STRENGTH,
                importance=imp,
            )
            factor.save()
            quadrant.factors.add(
                factor,
            )

        total_score = quadrant.get_total_score()
        self.assertEqual(
            total_score,
            25,
            msg=f"Quadrant `get_total_score` returned {total_score}, but it should return 25.",  # noqa
        )
