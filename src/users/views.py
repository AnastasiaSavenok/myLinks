import random

from django.contrib.auth import login, logout
from rest_framework import status, mixins, views
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.core.emails import sending_mail
from src.users.models import CustomUser
from src.users.serializers import LoginSerializer, RegisterSerializer, UserSerializer, EmailVerifySerializer


class LoginAPIView(mixins.CreateModelMixin, GenericAPIView):
    serializer_class = LoginSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request, CustomUser.objects.get(email=serializer.data['email']))
        return Response({'message': "Login successful"}, status=status.HTTP_200_OK)


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
                sending_mail(user.email, token)
                user.save()
                return Response({"Registration success. Please, verify email.":
                                UserSerializer(user, context=self.get_serializer_context()).data},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'Registration failed'}, status=status.HTTP_401_UNAUTHORIZED)


class EmailVerify(GenericAPIView):
    serializer_class = EmailVerifySerializer
    get_queryset = CustomUser.objects.all
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if request.user.verify_token == token and token != 00000:
            request.user.is_verify = True
            request.user.verify_token = 00000
            request.user.save()
            return Response({'message': "Verify success."}, status=status.HTTP_200_OK)
        return Response({'message': "Verify failed."}, status=status.HTTP_401_UNAUTHORIZED)
