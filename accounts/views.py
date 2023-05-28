from rest_framework.response import Response
from .models import User
from .serializers import RegistrationSerializer
from rest_framework import status
from rest_framework.views import APIView
import uuid
from .helper import send_verification_email,send_password_reset_email
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

class RegistrationView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.data['email'])
            token = str(uuid.uuid4())
            domain_name = get_current_site(request).domain
            relative_path = reverse("verify",args=[token])
            url = f"http://{domain_name}{relative_path}"
            user.verification_code = token
            user.save()
            email_sent = send_verification_email(user.email, url)
            if not email_sent:
                return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success':'an verification email has been sent to your email address'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmailVerificationView(APIView):
    def get(self, request,token):
        try:
            user = User.objects.get(verification_code=token)
        except User.DoesNotExist:
            return Response({'error':'Token is invalid or expired'}, status=status.HTTP_404_NOT_FOUND)
        user.is_verified = True
        user.verification_code = ""
        user.save()
        return Response({'success':'User has been verified'}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error':'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response({'error':'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_verified:
            return Response({'error':'User is not verified. Please verify your account first'}, status=status.HTTP_400_BAD_REQUEST)
        
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return Response({'token':str(token)}, status=status.HTTP_200_OK)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error':'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        token = str(uuid.uuid4())
        domain_name = get_current_site(request).domain
        relative_path = reverse("reset_password",args=[token])
        url = f"http://{domain_name}{relative_path}"
        user.pwd_reset_token = token
        user.save()
        email_sent = send_password_reset_email(user.email,url)
        if not email_sent:
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success':'An email has been sent to your account'}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request,token):
        try:
            user = User.objects.get(pwd_reset_token=token)
        except User.DoesNotExist:
            return Response({'error':'Token is invalid or expired'}, status=status.HTTP_404_NOT_FOUND)
        
        password = request.data['password']
        password2 = request.data['password2']
        
        if password != password2:
            return Response({'error':'Passwords do not match'},status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.save()
        return Response({'success':'Your password has been changed'}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = User.objects.get(email=request.user)
        current_password = request.data['current_password']
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password']

        if not user.check_password(current_password):
            return Response({'error':'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_password:
            return Response({'error':'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'success':'Your password has been changed'}, status=status.HTTP_200_OK)