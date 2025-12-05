from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from config import Config

from flask_socketio import SocketIO

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
socketio = SocketIO()
mail = Mail()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["2000 per day", "500 per hour"],
    storage_uri="memory://"
)
talisman = Talisman()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    socketio.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    
    # Configure Talisman (Security Headers)
    # Note: content_security_policy needs to allow inline scripts/styles for this template
    csp = {
        'default-src': '\'self\'',
        'script-src': ['\'self\'', '\'unsafe-inline\'', 'https://cdn.jsdelivr.net', 'https://cdnjs.cloudflare.com'],
        'style-src': ['\'self\'', '\'unsafe-inline\'', 'https://cdn.jsdelivr.net', 'https://cdnjs.cloudflare.com', 'https://fonts.googleapis.com'],
        'font-src': ['\'self\'', 'https://fonts.gstatic.com', 'https://cdnjs.cloudflare.com'],
        'img-src': ['\'self\'', 'data:', 'blob:'],
    }
    talisman.init_app(app, 
                      content_security_policy=csp, 
                      force_https=False,
                      session_cookie_secure=False, # Disable secure cookies for HTTP
                      strict_transport_security=False # Disable HSTS for HTTP
                      ) 
    
    # Exempt SocketIO from CSRF (it uses its own authentication)
    csrf.exempt('socketio')

    from app.routes import auth, main, admin, chat
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)

    # Make get_alerts available in all templates
    from app.utils.alerts import get_alerts
    from app.models import SystemSettings
    @app.context_processor
    def inject_context():
        settings = SystemSettings.query.first()
        # Fallback if no settings yet (shouldn't happen due to update script, but good for safety)
        if not settings:
            settings = SystemSettings() 
        return dict(get_alerts=get_alerts, system_settings=settings)

    return app
