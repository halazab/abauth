from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    # Password reset
    path('reset-password/', views.ResetPasswordEmailView.as_view(), name='reset_password'),
    path('reset-password/confirm/', views.ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
    
    # 2FA
    path('2fa/setup/', views.Setup2FAView.as_view(), name='setup_2fa'),
    path('2fa/verify/', views.Verify2FAView.as_view(), name='verify_2fa'),
] 