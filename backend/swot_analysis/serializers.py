"""
Serializer of the SWOTAnalysis model
"""
from rest_framework import serializers
from .models import SWOTAnalysis

# from user.serializers import UserSerializer


class SWOTAnalysisSerializer(serializers.ModelSerializer):

    # This is needed to display the string version of the state instead of integer version
    state = serializers.CharField(source="get_state_display", read_only=True)

    class Meta:
        model = SWOTAnalysis
        fields = "__all__"
        # Make user read only and not required
        extra_kwargs = {
            "user": {"read_only": True, "required": False},
        }

    # # Serialize user representation in JSON response
    # def to_representation(self, instance):
    #     self.fields["user"] = UserSerializer(read_only=True)
    #     return super(SWOTAnalysisSerializer, self).to_representation(instance)

    # Define user to currently logged in user
    def create(self, validated_data):
        # Assign user to currently logged-in user
        validated_data["user"] = self.context["request"].user
        return super(SWOTAnalysisSerializer, self).create(validated_data)