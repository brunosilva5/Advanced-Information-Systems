"""
Serializer of the Quadrant model
"""
from rest_framework import serializers
from ..models import Quadrant
from .factor_serializer import FactorSerializer
from django.utils.translation import ugettext_lazy as _


class QuadrantSerializer(serializers.ModelSerializer):

    # Display name string representation
    q_type = serializers.CharField(
        source="get_q_type_display",
    )

    # Add total score field
    total_score = serializers.FloatField(
        source="get_total_score",
        read_only=True,
    )

    # Serialize factors (nested serializer)
    factors = FactorSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Quadrant
        fields = "__all__"

    def _validate_q_type(self, q_type):
        """
        Performs validation for `q_type`
        """
        error_msg = serializers.ValidationError(
            {
                "q_type": _(
                    f"Invalid choice for q_type. Valid choices are (integer part): {Quadrant.QuadrandType.choices}",  # noqa
                ),
            }
        )

        # Make q_type integer, important for if statements
        try:
            q_type = int(q_type)
        except ValueError:
            raise error_msg

        # Check if valid choice
        if q_type not in [int(el[0]) for el in Quadrant.QuadrandType.choices]:
            raise error_msg
        return q_type

    def validate(self, attrs):
        """
        Performs validation for the model
        """
        # Validate `q_type`
        attrs["get_q_type_display"] = self._validate_q_type(
            attrs["get_q_type_display"],
        )
        return super().validate(attrs)

    def create(self, validated_data):
        # Replace `get_q_type_display` for
        # `q_type`
        validated_data["q_type"] = validated_data.pop("get_q_type_display")
        return super().create(validated_data)
