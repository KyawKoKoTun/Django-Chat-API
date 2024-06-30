from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *
from .otp_views import *

urlpatterns = [
    path("auth/register/", RegistrationView.as_view(), name="user_registration_view"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "auth/token/obtain/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("profile/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("auth/request-otp/", RequestOTPAPI.as_view(), name="request_otp"),
    path("auth/reset-password/", ResetPasswordAPI.as_view(), name="reset_password"),
    path("username/", UsernameAPIView.as_view(), name="api-username"),
]
