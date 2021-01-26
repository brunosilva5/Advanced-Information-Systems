"""
Serializer of the SWOTAnalysis model
"""
from rest_framework import serializers
from ..models import SWOTAnalysis
from .quadrant_serializer import QuadrantSerializer
from django.utils.translation import ugettext_lazy as _


class SWOTAnalysisSerializer(serializers.ModelSerializer):

    # This is needed to display the string version of
    #  the state instead of integer version
    state = serializers.CharField(
        source="get_state_display",
        required=False,
    )

    # Serialize quadrants (nested serializer)
    quadrants = QuadrantSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = SWOTAnalysis
        # Make user read only and not required
        extra_kwargs = {
            "user": {"read_only": True, "required": False},
        }
        optional_fields = [
            "state",
        ]
        exclude = ("user",)

    # Define user to currently logged in user
    def create(self, validated_data):
        # Assign user to currently logged-in user
        validated_data["user"] = self.context["request"].user

        # Prevent state for being assigned
        # (must use default, can only be updated)
        validated_data["state"] = (
            int(
                SWOTAnalysis.SWOTAnalysisStates.IN_PROGRESS,
            ),
        )[  # noqa
            0
        ]  # [0] because returns tuple of length 1
        # Delete "get_state_display" key
        validated_data.pop("get_state_display", None)

        return super(SWOTAnalysisSerializer, self).create(validated_data)

    def _validate_state(self, state):
        """
        Performs validation for `state`
        """
        error_msg = serializers.ValidationError(
            {
                "state": _(
                    f"Invalid choice for state. Valid choices are (integer part): {SWOTAnalysis.SWOTAnalysisStates.choices}",  # noqa
                ),
            }
        )

        # Parse state to int, important for if statements
        try:
            state = int(state)
        except ValueError:
            raise error_msg
        # Check if valid choice
        if state not in [
            int(el[0]) for el in SWOTAnalysis.SWOTAnalysisStates.choices
        ]:  # noqa
            raise error_msg

        return state

    def validate(self, attrs):
        if "get_state_display" in attrs:
            attrs["get_state_display"] = self._validate_state(
                attrs["get_state_display"],
            )
        return super().validate(attrs)

    def update(self, instance, validated_data):

        # Replace `get_state_display` key with `state`
        validated_data["state"] = validated_data.pop("get_state_display")
        return super().update(instance, validated_data)
