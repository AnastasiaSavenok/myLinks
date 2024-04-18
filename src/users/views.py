import random

from django.contrib.auth import login, logout
from rest_framework import status, mixins, views
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from src.core.emails import send_email
from src.core.permissions import IsVerified
from src.users.models import CustomUser
from src.users.serializers import LoginSerializer, RegisterSerializer, UserSerializer, EmailVerifySerializer, \
    ChangePasswordSerializer, RecoverPasswordSerializer, ForgotPasswordSerializer


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request, CustomUser.objects.get(email=request.data.get('email')))
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutAPIView(views.APIView):

    def post(self, request):
        logout(request)
        Response().delete_cookie(key="refreshToken")
        return Response({'message': "Logout successful"}, status=status.HTTP_200_OK)


class RegisterAPIView(mixins.CreateModelMixin, GenericAPIView):
    serializer_class = RegisterSerializer
    get_queryset = CustomUser.objects.all

    def post(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(email=request.data.get('email'))
            if user:
                return Response({'Email is already used'}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            if user:
                token = random.randint(11111, 99999)
                user.verify_token = token
                user.set_password(user.password)
                send_email(user.email, f'Verify code: {token}')
                user.save()
                return Response({"Registration success. Verify code sent to email.":
                                UserSerializer(user, context=self.get_serializer_context()).data},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'Registration failed'}, status=status.HTTP_401_UNAUTHORIZED)


class EmailVerify(GenericAPIView):
    serializer_class = EmailVerifySerializer
    get_queryset = CustomUser.objects.all
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = request.data.get('verify_token')
        if request.user.verify_token == token and token != 00000:
            request.user.is_verify = True
            request.user.verify_token = 00000
            request.user.save()
            return Response({'message': "Verify success."}, status=status.HTTP_200_OK)
        return Response({'message': "Verify failed."}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordAPIView(GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated, IsVerified)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(request.data.get('password'))
        request.user.save()
        return Response({'message': "Password changed."}, status=status.HTTP_200_OK)


class ForgotPasswordAPIView(GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = CustomUser.objects.get(email=request.data.get('email', None))
            if user:
                token = random.randint(11111, 99999)
                user.verify_token = token
                user.save()
                send_email(user.email, f'Verify code: {token}')
                return Response({'Verify code sent to this email'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'Email is not exist'}, status=status.HTTP_400_BAD_REQUEST)


class RecoverPasswordAPIView(GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RecoverPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.data.get('verify_token', 00000)
        try:
            user = CustomUser.objects.get(email=request.data.get('email', None))
            if str(user.verify_token) == token and token != 00000:
                new_password = str(random.randint(111111111, 999999999))
                user.set_password(new_password)
                user.verify_token = 00000
                user.save()
                send_email(user.email, f'Your password was changed. New password: {new_password}')
                return Response({f'Your new password: {new_password}'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'Email is not exist'}, status=status.HTTP_400_BAD_REQUEST)
