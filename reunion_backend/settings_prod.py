from .settings import *

# Production settings
DEBUG = False

# Update CORS settings for production
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

# Database configuration for production
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

import logging
logger = logging.getLogger(__name__)

def your_view(request):
    logger.debug(f"Received request: {request.method}")
    logger.debug(f"Request data: {request.data}")
    # ... rest of your view code 