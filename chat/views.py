from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Message, FileAttachment
from .serializers import MessageSerializer, FileAttachmentSerializer


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "text",
                openapi.IN_FORM,
                description="Message text",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "file_attachments",
                openapi.IN_FORM,
                description="File attachments",
                type=openapi.TYPE_FILE,
                required=False,
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        text = request.data.get("text")

        if not text:
            return Response(
                {"detail": "Text is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        message = Message.objects.create(user=user, text=text)

        files = request.FILES.getlist("file_attachments")
        for file in files:
            FileAttachment.objects.create(message=message, file=file)

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user).order_by("-created_at")
