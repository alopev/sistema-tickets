import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    # Security: Use strong SECRET_KEY from environment
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in environment variables (.env file)")
    
    # Database configuration
    db_password = os.environ.get('DB_PASSWORD')
    if db_password is None:
        raise ValueError("DB_PASSWORD must be set in environment variables (.env file)")
    
    password = quote_plus(db_password)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'mysql+mysqlconnector://root:{password}@localhost/ticket_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16MB max limit
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@helpdesk.com'
    
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # No time limit for CSRF tokens

    # Session Configuration
    from datetime import timedelta
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # Changed from 5 to 30 minutes
    SESSION_REFRESH_EACH_REQUEST = True
    
    # Flask-Security-Too Configuration
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or SECRET_KEY
    SECURITY_REGISTERABLE = False  # Disable public registration
    SECURITY_RECOVERABLE = True  # Enable password recovery
    SECURITY_CHANGEABLE = True  # Enable password change
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = True
    SECURITY_SEND_PASSWORD_RESET_EMAIL = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_TRACKABLE = True  # Track user login info
