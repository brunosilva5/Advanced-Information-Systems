from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from ..serializers import QuadrantSerializer


class QuadrantView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    """
    View for operations on a analysis quadrant.
    * Requires Authenticated User
    """

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = QuadrantSerializer

    def post(self, request, *args, **kwargs):
        """
        POST method to create an SWOTAnalysis for currently logged in user.
        """
        # need to pass the request in context,
        # so the serializer can acess current user
        serializer = QuadrantSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
