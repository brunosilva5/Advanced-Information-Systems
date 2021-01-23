"""
User related views
"""
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import mixins, generics


from .serializers import UserSerializer, GetTokenSerializer


class CreateUserView(APIView):
    """
    View to create a new user

    * Anonymous user can acess this view
    """

    # Allow any user to acess this view
    permission_classes = [AllowAny]

    def post(self, request, format=None):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(TokenObtainPairView):
    """
    Override TokenObtainPairView to use the custom serializer
    """

    serializer_class = GetTokenSerializer


class DetailUserView(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    """
    View for operations on a specific user's personal profile.
    * Requires Authenticated User
    """

    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer

    def get_object(self):
        """
        A user should only be able to manage himself
        """
        return self.request.user

    def delete(self, request, *args, **kwargs):
        """Deleting the currently logged-in user"""
        # Delete the user
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
