# """
# Contains unit-tests for the Factor model
# """
# from django.test import TestCase
# from django.core.exceptions import ValidationError

# from ..factor import Factor


# class FactorTestCase(TestCase):
#     def test_description_max_limit(self):
#         """
#         Tests if the factor description char limit is 50
#         """
#         with self.assertRaises(ValidationError) as exc:
#             factor = Factor(description="a" * 51)
#             factor.full_clean()

#         exception = exc.exception
#         self.assertIn("description", exception.error_dict)
#         description_exceptions = exception.error_dict["description"]
#         self.assertEqual(1, len(description_exceptions))
#         description_exception = description_exceptions[0]
#         self.assertEqual("max_length", description_exception.code)

#     # def test_factor_invalid_importance_choice(self):
#     #     """
#     #     Tests
#     #     """