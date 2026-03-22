"""
WIL Management System Configuration
Production-ready configuration with security best practices
"""

import os
from datetime import timedelta

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration class with common settings"""
    
    # ============================================
    # SECURITY SETTINGS
    # ============================================
    
    # Secret key for session management and CSRF protection
    # In production, set this as environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-super-secret-key-change-in-production'
    
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY') or 'csrf-secret-key'
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True  # Only send over HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # ============================================
    # DATABASE CONFIGURATION
    # ============================================
    
    # SQLite Database (for development and small deployments)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'database', 'wil_system.db')
    
    # For PostgreSQL in production:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'postgresql://user:password@localhost/wil_system'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
    
    # ============================================
    # FILE UPLOAD CONFIGURATION
    # ============================================
    
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        'document': {'pdf', 'doc', 'docx', 'txt'},
        'image': {'png', 'jpg', 'jpeg', 'gif'},
        'resume': {'pdf', 'doc', 'docx'}
    }
    
    # ============================================
    # EMAIL CONFIGURATION (SMTP)
    # ============================================
    
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@wil-system.ac.za'
    
    # ============================================
    # APPLICATION SETTINGS
    # ============================================
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # Application Limits
    MAX_APPLICATIONS_PER_STUDENT = 10
    
    # Deadline Reminder (days before)
    DEADLINE_REMINDER_DAYS = 3
    
    # ============================================
    # POPIA COMPLIANCE SETTINGS
    # ============================================
    
    # Data retention period (days)
    DATA_RETENTION_DAYS = 2555  # 7 years
    
    # Require explicit consent
    POPIA_CONSENT_REQUIRED = True
    
    # Privacy policy URL
    PRIVACY_POLICY_URL = '/privacy-policy'
    
    # ============================================
    # LOGGING CONFIGURATION
    # ============================================
    
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')
    
    # ============================================
    # EXTERNAL API KEYS
    # ============================================
    
    # Google OAuth (optional)
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    # SMS Gateway API (optional)
    SMS_API_KEY = os.environ.get('SMS_API_KEY')
    SMS_API_URL = os.environ.get('SMS_API_URL')
    
    # ============================================
    # MAINTENANCE MODE
    # ============================================
    
    MAINTENANCE_MODE = os.environ.get('MAINTENANCE_MODE', 'false').lower() == 'true'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development
    SQLALCHEMY_ECHO = True  # Log SQL queries
    
    # Use a simpler secret key for development
    SECRET_KEY = 'dev-secret-key-not-for-production'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
    # Use in-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Disable email sending in tests
    MAIL_SUPPRESS_SEND = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Ensure all security settings are enabled
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    
    # Stricter CSRF
    WTF_CSRF_TIME_LIMIT = 1800  # 30 minutes
    
    # Production database (PostgreSQL recommended)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Logging
    LOG_LEVEL = 'WARNING'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}