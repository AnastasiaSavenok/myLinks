from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from src.users.models import CustomUser


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = CustomUser.objects.get(email=email)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = CustomUser.objects.create_user(email=validated_data['email'],
                                                  password=validated_data['password']
                                                  )
            user.save()
            return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email',)


class EmailVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('verify_token',)
