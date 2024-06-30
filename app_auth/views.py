from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import *
from django.db.utils import IntegrityError

class RegistrationView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.create(serializer.validated_data)
                user.save()
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                return Response(
                    {
                        "message": "Registration successful",
                        "user": CustomUserSerializer(user).data,
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:
                return Response(
                    {
                        "message": "Account with that email already exists",
                    },
                    status=status.HTTP_409_CONFLICT,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenVerifyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Extract IP address from request
        ip_address = self.get_client_ip(request)

        # Update last login IP of the user
        user.last_login_ip = ip_address
        user.save(update_fields=["last_login_ip"])

        try:
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)

        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class UserUpdateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsernameAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "User ID is required."}, status=400)

        try:
            user = User.objects.get(user_id=user_id)
            return Response({"username": user.username})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
