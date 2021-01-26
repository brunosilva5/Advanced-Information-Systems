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

    def test_quadrant_invalid_q_type_choices(self):
        """
        Tests the quadrant name choices
        """
        # Create a list with all digits
        all_choices = list(map(int, list(string.digits)))
        # Create a list with valid choices
        valid_choices = [1, 2, 3, 4]

        # Iterate over all possible choices
        for c in all_choices:
            # If `c` not a valid choice
            # ensure that a exception is raised
            if c not in valid_choices:
                with self.assertRaises(ValidationError) as exc:
                    quadrant = Quadrant(q_type=c)
                    quadrant.full_clean()

                exception = exc.exception
                self.assertIn("q_type", exception.error_dict)
                q_type_exceptions = exception.error_dict["q_type"]
                self.assertEqual(1, len(q_type_exceptions))
                q_type_exception = q_type_exceptions[0]
                self.assertEqual("invalid_choice", q_type_exception.code)

    def test_no_duplicate_quadrants(self):
        """
        Tests that a analysis can't have duplicate quadrants.
        Check: https://stackoverflow.com/questions/21458387/transactionmanagementerror-you-cant-execute-queries-until-the-end-of-the-atom
        """  # noqa

        valid_choices = [1, 2, 3, 4]

        for c in valid_choices:
            # Create quadrant
            Quadrant.objects.create(q_type=c, analysis=self.analysis)
            try:
                with transaction.atomic():
                    # Duplicates should be prevented.
                    Quadrant.objects.create(q_type=c, analysis=self.analysis)
                self.fail("Duplicate quadrants should not be allowed.")
            except IntegrityError:
                pass

    def test_internal_external_quadrants(self):
        """
        Tests if a quadrant is correctly classified as internal/external
        """
        internal_types = [1, 2]
        external_types = [3, 4]

        for t in internal_types:
            quadrant = Quadrant.objects.create(
                q_type=t,
                analysis=self.analysis,
            )
            self.assertTrue(
                quadrant.is_internal(),
                "Quadrant call to `is_internal` did not correctly classify as internal",  # noqa
            )

        for t in external_types:
            quadrant = Quadrant.objects.create(
                q_type=t,
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
            q_type=Quadrant.QuadrandType.STRENGTHS,
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
