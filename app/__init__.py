


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from sqlalchemy import text
import time

load_dotenv(override=True)

print(f"Current working directory: {os.getcwd()}")
print(f"DATABASE_URL found: {'Yes' if os.environ.get('DATABASE_URL') else 'No'}")

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

def wake_up_database(app):
    max_retries = 10
    retry_delay = 2
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.session.execute(text("SELECT 1"))
                print("Database is awake and responsive")
                return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Database not ready (attempt {attempt + 1}/{max_retries}), retrying...")
                time.sleep(retry_delay)
            else:
                print(f"Database failed to wake up: {e}")
                return False
    return False

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    raw_db_url = os.environ.get('DATABASE_URL')
    if not raw_db_url:
        raise ValueError("DATABASE_URL environment variable is required")
    
    # Normalize PostgreSQL URL to use psycopg3 driver
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif raw_db_url.startswith("postgresql://"):
        raw_db_url = raw_db_url.replace("postgresql://", "postgresql+psycopg://", 1)
    
    # Add sslmode if not present
    if "sslmode" not in raw_db_url:
        separator = "&" if "?" in raw_db_url else "?"
        raw_db_url += f"{separator}sslmode=require"
    
    print(f"Using database URL: {raw_db_url}")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 5,
        'max_overflow': 10,
        'connect_args': {'sslmode': 'require', 'connect_timeout': 10}
    }
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'admin.login'
    login_manager.login_message_category = 'info'
    
    with app.app_context():
        wake_up_database(app)
    
    from app.routes import main, products, blog, admin, demos, gallery, privacy
    app.register_blueprint(main.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(demos.bp)
    app.register_blueprint(gallery.bp)
    app.register_blueprint(privacy.bp)
    
    @app.context_processor
    def inject_settings():
        try:
            from app.models.settings import SiteSettings
            settings = SiteSettings.query.first()
            admin_user = None
            try:
                from app.models.user import User
                admin_user = User.query.first()
            except:
                pass
            return dict(site_settings=settings, admin=admin_user)
        except:
            return dict(site_settings=None, admin=None)
    
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))




