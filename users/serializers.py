from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        
        # Normalize email to lowercase
        attrs['email'] = attrs['email'].lower()

        # Check if email already exists
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email address already exists")

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password from validated_data
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)
