"""
Serializer of the Quadrant model
"""
from rest_framework import serializers
from ..models import Quadrant
from .factor_serializer import FactorSerializer


class QuadrantSerializer(serializers.ModelSerializer):

    # Display name string representation
    name = serializers.CharField(
        source="get_name_display",
        read_only=True,
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
