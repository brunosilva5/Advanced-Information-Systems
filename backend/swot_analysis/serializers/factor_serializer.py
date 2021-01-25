"""
Serializer of the Factor model

"""
from rest_framework import serializers
from ..models import Factor


class FactorSerializer(serializers.ModelSerializer):

    # Add score field
    score = serializers.CharField(source="get_score", read_only=True)

    # Display name string representation
    importance = serializers.CharField(
        source="get_importance_display",
        read_only=True,
    )

    # Display name string representation
    classification = serializers.CharField(
        source="get_classification_display",
        read_only=True,
    )

    class Meta:
        model = Factor
        fields = "__all__"
