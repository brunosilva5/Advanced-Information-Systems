"""
Module containing all the endpoints related to Quadrant model
"""
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404


from ..serializers import QuadrantSerializer

from ..models import Quadrant, SWOTAnalysis


class QuadrantViewSet(viewsets.ViewSet):
    """
    Viewset to manage Quadrants of a particular SWOTAnalysis,
    for the currently authenticated user.
    """

    # Serializer class of this view
    serializer_class = QuadrantSerializer
    # Queryset of this view
    queryset = Quadrant.objects.all()
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
            return Quadrant.objects.none()

        # Grab analysis id
        analysis_id = self.kwargs["swot_analysis_pk"]
        # First we get the analysis by id and belonging to current user
        analysis = get_object_or_404(
            SWOTAnalysis.objects.filter(user=self.request.user),
            pk=analysis_id,
        )

        # Now we return all the quadrants of the found analysis
        return analysis.quadrants

    def list(self, request, swot_analysis_pk):
        """
        Method for listing the quadrants of an analysis
        """
        queryset = self.get_queryset()
        serializer = QuadrantSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, swot_analysis_pk):
        """
        Method for creating a quadrant for a particular analysis
        of the currently authenticated user.
        """
        # Add analysis key to request
        data = request.data
        data.update({"analysis": swot_analysis_pk})
        serializer = QuadrantSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:  # noqa (The message varies depending on the database engine)
                raise ValidationError(
                    {
                        "q_type": [
                            "You already have a quadrant of this type.",
                        ],
                    }
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, swot_analysis_pk=None):
        """
        Returns a particular quadrant of a specific analysis
        (of the currently authenticated user)
        by given primary key.
        """
        qs = self.get_queryset()
        quadrant = get_object_or_404(qs, pk=pk)
        serializer = QuadrantSerializer(quadrant)
        return Response(serializer.data)
