from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .models import *


class RequestOTPAPI(APIView):
    def post(self, request):
        email = request.data.get('email')  # Get email from request data
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        otp_obj, created = OTP.objects.get_or_create(user=user)

        otp = otp_obj.get_token()

        # Send OTP via email
        subject = 'OneStep OTP for Password Reset'
        message = f'Your password reset OTP code is:<br> <h2><strong>{otp}</strong></h2>'
        from_email = 'kyawkokotunmm475157@gmail.com'  # Replace with your email
        recipient_list = [email]

        send_mail(subject=subject, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html_message=message, message='')

        return Response({'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)


class ResetPasswordAPI(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        otp_obj = OTP.objects.get(user=user)

        if not otp_obj.verify(otp):
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
