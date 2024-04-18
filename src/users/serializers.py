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


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def post(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    def validate(self, data):
        email = data.get('email')
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        return data


class RecoverPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    verify_token = serializers.CharField(max_length=10)

    def validate(self, data):
        email = data.get('email')
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        return data
