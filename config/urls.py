"""
URL configuration for xOneProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from rest_framework.routers import DefaultRouter

from src.users.views import LogoutAPIView, LoginAPIView, RegisterAPIView, EmailVerify, ChangePasswordAPIView, \
    ForgotPasswordAPIView, RecoverPasswordAPIView
from src.links.views import LinkViewSet, CollectionViewSet, TopUsersView, TestDataView

router = DefaultRouter()
router.register(r'links', LinkViewSet, basename='link')
router.register(r'collections', CollectionViewSet, basename='collection')

urlpatterns = [
    # Admin API
    path('admin/', admin.site.urls),

    # Auth API
    path('api/v1/change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('api/v1/forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('api/v1/recover-password/', RecoverPasswordAPIView.as_view(), name='forgot_password'),
    path('api/v1/logout/', LogoutAPIView.as_view(), name='logging_out'),
    path('api/v1/login/', LoginAPIView.as_view(), name='logging_in'),
    path('api/v1/register/', RegisterAPIView.as_view(), name="sign_up"),
    path('api/v1/verify-email/', EmailVerify.as_view(), name='verify_email'),

    # SQL task API
    path('api/v1/top-ten-users/', TopUsersView.as_view(), name='top_ten_users'),
    path('api/v1/test-data/', TestDataView.as_view(), name='test_data'),

    # Links API
    path('api/v1/', include(router.urls)),

    # Swagger API
    path('api/v1/docs/download/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/v1/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/v1/docs/specific/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]
