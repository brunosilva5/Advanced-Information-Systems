"""
Serializer of the Factor model

"""
from rest_framework import serializers
from ..models import Factor
from django.utils.translation import ugettext_lazy as _


class FactorSerializer(serializers.ModelSerializer):

    # Add score field
    score = serializers.CharField(source="get_score", read_only=True)

    # Display name string representation
    importance = serializers.CharField(
        source="get_importance_display",
    )

    # Display name string representation
    classification = serializers.CharField(source="get_classification_display")

    class Meta:
        model = Factor
        fields = "__all__"

    def _validate_classification(self, classification, quadrant):
        """
        Validates `classification` field based on quadrant.
        """
        error_msg = serializers.ValidationError(
            {
                "classification": _(
                    f"An internal factor can only have the following classifications: {list(map(Factor.FactorClassification.choices.__getitem__,allowed))}",  # noqa
                ),
            }
        )
        # Make classification integer, important for if statements
        try:
            classification = int(classification)
        except ValueError:
            raise error_msg

        if quadrant.is_internal():
            allowed = [
                int(Factor.FactorClassification.STRENGTH),
                int(Factor.FactorClassification.WEAKNESS),
            ]
            if classification not in allowed:
                raise error_msg

        elif quadrant.is_external():
            # An external factor can only have one of the
            # following classifications: ["Threat", "Opportunity"]
            allowed = [
                int(Factor.FactorClassification.THREAT),
                int(Factor.FactorClassification.OPPORTUNITY),
            ]
            if classification not in allowed:
                raise error_msg

        return classification

    def _validate_importance(self, importance):
        valid_values = Factor.FactorImportance.choices
        if not importance.isdigit():
            raise serializers.ValidationError(
                {
                    "importance": _(
                        f"This field should be one of the following (integer part): {valid_values}",  # noqa
                    ),
                }
            )
        return int(importance)

    def validate(self, attrs):
        """
        Performs validation for the model
        """
        # An internal factor can only have one of the
        # following classifications: ["Strength", "Weakness"]
        attrs["get_classification_display"] = self._validate_classification(
            attrs["get_classification_display"],
            attrs["quadrant"],
        )

        attrs["get_importance_display"] = self._validate_importance(
            attrs["get_importance_display"]
        )
        return super().validate(attrs)

    def create(self, validated_data):

        # Replace `get_classification_display` for
        # `classification`
        validated_data["classification"] = validated_data.pop(
            "get_classification_display"
        )

        # Replace `get_importance_display` for
        # `importance`
        validated_data["importance"] = validated_data.pop(
            "get_importance_display",
        )
        return super().create(validated_data)
