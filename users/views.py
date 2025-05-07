from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
import io
import base64
from datetime import timedelta

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    ResetPasswordEmailSerializer,
    ResetPasswordConfirmSerializer
)
from .models import CustomUser

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            # Send welcome email
            send_mail(
                'Welcome to Our Platform',
                f'Hi {user.get_full_name()},\n\nWelcome to our platform! Please verify your email to get started.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            return Response({
                'user': UserProfileSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = CustomUser.objects.get(email=email)
                
                # Check if account is locked
                if user.account_locked:
                    if user.account_locked_until and user.account_locked_until > timezone.now():
                        return Response({
                            'error': 'Account is locked. Please try again later.'
                        }, status=status.HTTP_403_FORBIDDEN)
                    else:
                        user.reset_failed_login()
                
                user = authenticate(email=email, password=password)
                
                if user:
                    if user.is_2fa_enabled:
                        # Generate and send 2FA code
                        device = devices_for_user(user, confirmed=True).first()
                        if not device:
                            device = TOTPDevice.objects.create(user=user, confirmed=True)
                        
                        return Response({
                            'message': '2FA required',
                            'user_id': user.id
                        }, status=status.HTTP_200_OK)
                    
                    refresh = RefreshToken.for_user(user)
                    user.reset_failed_login()
                    user.last_login_ip = request.META.get('REMOTE_ADDR')
                    user.save()
                    
                    return Response({
                        'user': UserProfileSerializer(user).data,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
                else:
                    user.increment_failed_login()
                    if user.failed_login_attempts >= 5:
                        user.account_locked = True
                        user.account_locked_until = timezone.now() + timedelta(minutes=30)
                        user.save()
                        return Response({
                            'error': 'Too many failed attempts. Account locked for 30 minutes.'
                        }, status=status.HTTP_403_FORBIDDEN)
                    
                    return Response({
                        'error': 'Invalid credentials'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                    
            except CustomUser.DoesNotExist:
                return Response({
                    'error': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({
                    'error': 'Wrong password'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({
                'message': 'Password updated successfully'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordEmailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                # Generate password reset token
                token = RefreshToken.for_user(user)
                reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
                
                # Send reset email
                send_mail(
                    'Password Reset Request',
                    f'Click the following link to reset your password: {reset_url}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                return Response({
                    'message': 'Password reset email sent'
                }, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({
                    'error': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirmView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = serializer.validated_data['token']
                refresh = RefreshToken(token)
                user = CustomUser.objects.get(id=refresh['user_id'])
                
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                
                return Response({
                    'message': 'Password reset successful'
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'error': 'Invalid or expired token'
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Setup2FAView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        device = devices_for_user(user, confirmed=True).first()
        
        if not device:
            device = TOTPDevice.objects.create(user=user, confirmed=True)
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(device.config_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_code = base64.b64encode(buffer.getvalue()).decode()
        
        return Response({
            'qr_code': qr_code,
            'secret_key': device.key
        })

    def post(self, request):
        user = request.user
        token = request.data.get('token')
        
        device = devices_for_user(user, confirmed=True).first()
        if device and device.verify_token(token):
            user.is_2fa_enabled = True
            user.save()
            return Response({
                'message': '2FA enabled successfully'
            })
        return Response({
            'error': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)

class Verify2FAView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user_id = request.data.get('user_id')
        token = request.data.get('token')
        
        try:
            user = CustomUser.objects.get(id=user_id)
            device = devices_for_user(user, confirmed=True).first()
            
            if device and device.verify_token(token):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': UserProfileSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND) 