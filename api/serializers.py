from rest_framework import serializers
from api.models import Profile, Code


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = "__all__"
