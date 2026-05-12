from .models import CustomUser
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'name', 'date_of_birth')

    def create(self, validated_data):
        
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)

        user.set_password(password)

        user.save()
       
        return user
    