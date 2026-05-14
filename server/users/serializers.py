from rest_framework import serializers

from .models import CustomUser

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:

        model = CustomUser

        fields = [
            'email',
            'password',
            'name',
            'date_of_birth'
        ]


    def create(self, validated_data):

        return CustomUser.objects.create_user(
            **validated_data
        )


class CustomTokenObtainPairSerializer(
    TokenObtainPairSerializer
):

    username_field = 'email'