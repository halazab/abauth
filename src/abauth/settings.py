"""
Default settings for abauth package.
"""

from datetime import timedelta

ABAUTH_SETTINGS = {
    # User model
    'AUTH_USER_MODEL': 'abauth.CustomUser',
    
    # JWT settings
    'JWT_AUTH': {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
        'ROTATE_REFRESH_TOKENS': True,
        'BLACKLIST_AFTER_ROTATION': True,
    },
    
    # Account security
    'ACCOUNT_SECURITY': {
        'MAX_LOGIN_ATTEMPTS': 5,
        'LOCKOUT_DURATION': timedelta(minutes=30),
        'PASSWORD_MIN_LENGTH': 8,
        'REQUIRE_SPECIAL_CHARACTERS': True,
        'REQUIRE_NUMBERS': True,
        'REQUIRE_UPPERCASE': True,
        'REQUIRE_LOWERCASE': True,
    },
    
    # Rate limiting
    'RATE_LIMITING': {
        'ANON_RATE': '100/day',
        'USER_RATE': '1000/day',
    },
    
    # Email verification
    'EMAIL_VERIFICATION': {
        'REQUIRED': True,
        'TIMEOUT_DAYS': 7,
    },
    
    # Two-factor authentication
    '2FA': {
        'REQUIRED_FOR_ADMIN': True,
        'ISSUER_NAME': 'ABAuth',
    },
    
    # Social authentication
    'SOCIAL_AUTH': {
        'GOOGLE_ENABLED': True,
        'GITHUB_ENABLED': True,
    },
    
    # Templates
    'TEMPLATES': {
        'LOGIN': 'abauth/login.html',
        'REGISTER': 'abauth/register.html',
        'PROFILE': 'abauth/profile.html',
        'PASSWORD_RESET': 'abauth/password_reset.html',
        'PASSWORD_RESET_CONFIRM': 'abauth/password_reset_confirm.html',
        '2FA_SETUP': 'abauth/2fa_setup.html',
    },
    
    # URLs
    'URLS': {
        'LOGIN_REDIRECT': '/',
        'LOGOUT_REDIRECT': '/',
        'PASSWORD_RESET_REDIRECT': '/login/',
    },
}

# Function to get settings with defaults
def get_setting(setting_name):
    from django.conf import settings
    
    user_settings = getattr(settings, 'ABAUTH_SETTINGS', {})
    default_settings = ABAUTH_SETTINGS.copy()
    
    if setting_name in user_settings:
        if isinstance(user_settings[setting_name], dict):
            default_settings[setting_name].update(user_settings[setting_name])
        else:
            default_settings[setting_name] = user_settings[setting_name]
    
    return default_settings[setting_name] 