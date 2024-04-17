from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from src.users.models import CustomUser


class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email

        return token


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
