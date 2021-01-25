from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from ..serializers import SWOTAnalysisSerializer


class SWOTAnalysisView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    """
    View for operations on a specific client's personal profile.
    * Requires Authenticated User
    """

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = SWOTAnalysisSerializer

    def post(self, request, *args, **kwargs):
        """
        POST method to create an SWOTAnalysis for currently logged in user.
        """
        # need to pass the request in context,
        # so the serializer can acess current user
        serializer = SWOTAnalysisSerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
