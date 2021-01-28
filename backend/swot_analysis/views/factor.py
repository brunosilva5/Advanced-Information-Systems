"""
API Endpoints for Factor model
"""
from rest_framework import permissions, status
from rest_framework.response import Response
from swot_analysis.serializers.factor_serializer import FactorSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from ..models import Factor, SWOTAnalysis, Quadrant


class FactorViewSet(viewsets.ViewSet):
    """
    A Viewset to create or delete a factor
    """

    # Serializer class of this view
    serializer_class = FactorSerializer
    # Queryset of this view
    queryset = Factor.objects.all()
    # Permission classes of this view
    permission_classes = [
        # Only allow authenticated users
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        """
        This view should only return quadrants a particular SWOTAnalysis,
        that has the primary key in url.
        """
        # https://github.com/axnsan12/drf-yasg/issues/333
        if getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            return Factor.objects.none()

        # Grab analysis id and quadrant id
        quadrant_id = self.kwargs["quadrant_pk"]
        analysis_id = self.kwargs["swot_analysis_pk"]
        # First we get the analysis by id and belonging to current user
        analysis = get_object_or_404(
            SWOTAnalysis.objects.filter(user=self.request.user),
            pk=analysis_id,
        )

        # Now we check if current quadrant belongs to the analysis
        quadrant = get_object_or_404(analysis.quadrants, pk=quadrant_id)

        # Now we get all the factors of the found quadrant
        return quadrant.factors

    def list(self, request, quadrant_pk, swot_analysis_pk):
        """
        Method for listing the factors of a quadrant
        """
        queryset = self.get_queryset()
        serializer = FactorSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, swot_analysis_pk, quadrant_pk):
        """
        Method for creating a factor for a particular quadrant
        of a particular analysis of the currently authenticated user.
        """
        # Add analysis key to request
        data = request.data
        data.update({"quadrant": quadrant_pk})
        serializer = FactorSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:
                quadrant = get_object_or_404(
                    Quadrant.objects.all(),
                    pk=quadrant_pk,
                ).get_q_type_display()
                raise ValidationError(
                    {
                        "description": [
                            f"Quadrant {quadrant} already has a factor with this description.",  # noqa
                        ],
                    }
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, swot_analysis_pk, quadrant_pk, pk=None):
        """
        Method for deleting a factor for a particular quadrant
        of a particular analysis of the currently authenticated user.
        """
        qs = self.get_queryset()
        factor = get_object_or_404(qs, pk=pk)
        factor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
