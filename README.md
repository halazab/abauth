# Advanced Django Authentication System (ABAuth)

A comprehensive authentication system for Django with advanced security features, built on top of Django REST Framework.

## Features

- 🔐 Custom User Model with Extended Fields
- 📧 Email-based Authentication
- 🔑 JWT Token Authentication
- 🔒 Two-Factor Authentication (2FA)
- 🔄 Password Reset Functionality
- 🛡️ Account Security Features
  - Login Attempt Tracking
  - Account Locking
  - IP Tracking
- 📱 Social Authentication (Google, GitHub)
- 👤 Profile Management
- 📸 Profile Picture Support
- 🔄 Session Management
- ⚡ Rate Limiting
- 🔒 Security Headers

## Quick Installation

```bash
pip install abauth
```

## Configuration

1. Add 'abauth' to your INSTALLED_APPS in settings.py:

```python
INSTALLED_APPS = [
    ...
    'abauth',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]
```

2. Set the custom user model in settings.py:

```python
AUTH_USER_MODEL = 'abauth.CustomUser'
```

3. Configure ABAuth settings (optional):

```python
ABAUTH_SETTINGS = {
    'ACCOUNT_SECURITY': {
        'MAX_LOGIN_ATTEMPTS': 5,
        'LOCKOUT_DURATION': timedelta(minutes=30),
    },
    'RATE_LIMITING': {
        'ANON_RATE': '100/day',
        'USER_RATE': '1000/day',
    },
    'EMAIL_VERIFICATION': {
        'REQUIRED': True,
    },
    '2FA': {
        'REQUIRED_FOR_ADMIN': True,
    },
}
```

4. Add ABAuth URLs to your urls.py:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('auth/', include('abauth.urls')),
]
```

5. Run migrations:

```bash
python manage.py migrate
```

## API Endpoints

### Authentication
- `POST /auth/register/` - Register a new user
- `POST /auth/login/` - Login user
- `POST /auth/token/refresh/` - Refresh JWT token

### Profile Management
- `GET/PUT /auth/profile/` - Get/Update user profile
- `POST /auth/change-password/` - Change password

### Password Reset
- `POST /auth/reset-password/` - Request password reset
- `POST /auth/reset-password/confirm/` - Confirm password reset

### Two-Factor Authentication
- `GET /auth/2fa/setup/` - Setup 2FA
- `POST /auth/2fa/verify/` - Verify 2FA token

## Customization

### Templates
You can override any of the default templates by creating your own in your project's templates directory:

```
templates/
    abauth/
        login.html
        register.html
        profile.html
        password_reset.html
        password_reset_confirm.html
        2fa_setup.html
```

### Settings
All settings are customizable through the `ABAUTH_SETTINGS` dictionary in your Django settings:

```python
ABAUTH_SETTINGS = {
    'TEMPLATES': {
        'LOGIN': 'myapp/custom_login.html',
    },
    'URLS': {
        'LOGIN_REDIRECT': '/dashboard/',
    },
    # ... other settings
}
```

## Security Features

### Password Requirements
- Minimum 8 characters
- Must contain letters and numbers
- Cannot be too similar to user information
- Cannot be a common password

### Account Protection
- Account locking after 5 failed login attempts
- 30-minute lockout period
- IP address tracking
- Session management
- Rate limiting

### Two-Factor Authentication
- TOTP-based 2FA
- QR code generation
- Backup codes support

## Social Authentication

To enable social authentication:

1. Configure OAuth credentials in Django admin
2. Enable providers in settings:

```python
ABAUTH_SETTINGS = {
    'SOCIAL_AUTH': {
        'GOOGLE_ENABLED': True,
        'GITHUB_ENABLED': True,
    }
}
```

## Production Deployment

Before deploying to production:

1. Set secure settings:
```python
ABAUTH_SETTINGS = {
    'SECURITY': {
        'SECURE_SSL_REDIRECT': True,
        'SESSION_COOKIE_SECURE': True,
        'CSRF_COOKIE_SECURE': True,
    }
}
```

2. Configure proper email settings
3. Set up a production database
4. Configure proper CORS settings
5. Set up proper static and media file serving

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 