# Additional settings to append to settings.py

# Static files configuration
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Time zone
TIME_ZONE = 'Asia/Kolkata'
