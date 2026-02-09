"""
Production Security Settings
Add these to your settings.py when deploying to production
"""

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set to False in production

# SECURITY WARNING: keep the secret key used in production secret!
# In production, use environment variable: os.environ.get('SECRET_KEY')
SECRET_KEY = 'django-insecure-your-secret-key-here'

# Production security settings
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Add your domain in production

# Security Middleware Settings (uncomment for production)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'

# Session Security
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_HTTPONLY = True

# Password Validation (already in settings.py, but these are important)
# Strong password requirements are enforced

# HTTPS Settings (for production)
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
