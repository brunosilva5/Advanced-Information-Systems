"""
Module containing all the endpoints related to SWOTAnalysis model
"""
from swot_analysis.models.swot_analysis import SWOTAnalysis
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from ..serializers import SWOTAnalysisSerializer
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class SWOTAnalysisViewSet(viewsets.ViewSet):
    """
    Viewset to manage SWOT Analysis for the currently authenticated user.
    """

    # Serializer class of this view
    serializer_class = SWOTAnalysisSerializer
    # Queryset of this view
    queryset = SWOTAnalysis.objects.all()
    # Permission classes of this view
    permission_classes = [
        # Only allow authenticated users
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        """
        This view should only return a list of all the swot analysis
        for the currently authenticated user.
        """

        # https://github.com/axnsan12/drf-yasg/issues/333
        if getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            return SWOTAnalysis.objects.none()

        return SWOTAnalysis.objects.filter(user=self.request.user)

    def list(
        self,
        request,
    ):
        """
        Returns all the analyses for the currently authenticated user.
        """
        queryset = self.get_queryset()
        serializer = SWOTAnalysisSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Returns a particular analysis (of the currently authenticated user)
        by given primary key.
        """
        qs = self.get_queryset()
        analysis = get_object_or_404(qs, pk=pk)
        serializer = SWOTAnalysisSerializer(analysis)
        return Response(serializer.data)

    def create(self, request):
        """
        Create an analysis for the currently authenticated user.
        """
        # need to pass the request in context,
        # so the serializer can acess current user
        serializer = SWOTAnalysisSerializer(
            data=request.data,
            context={"request": request},
        )
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
                        "title": [
                            "You already have an analysis with this name.",
                        ],
                    }
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Method for deleting a particular analysis for
        the currently authenticated user.
        """
        analysis = self.queryset.get(pk=pk)
        analysis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        """
        Method for partially updating a particular analysis
        for the currently authenticated user.
        """
        serializer = SWOTAnalysisSerializer(
            self.get_queryset().get(pk=pk), data=request.data, partial=True
        )
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK,
                )
            except IntegrityError:  # noqa (The message varies depending on the database engine)
                raise ValidationError(
                    {
                        "title": [
                            "You already have an analysis with this name.",
                        ],
                    }
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
