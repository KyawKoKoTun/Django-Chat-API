from rest_framework import generics, status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User, Contact
from .serializers import ContactSerializer


class AddContactView(generics.CreateAPIView):
    serializer_class = ContactSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="User ID of the contact to be added",
                )
            },
        )
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {"detail": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            contact = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        contact_data = {"user": request.user.id, "contact": contact.id}
        serializer = self.get_serializer(data=contact_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateUserActivityView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        user.last_active = timezone.now()
        user.save()
        return Response({"status": "last active updated"})
