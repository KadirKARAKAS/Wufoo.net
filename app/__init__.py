# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'routes.login'
login_manager.login_message_category = 'info'
migrate = Migrate()

class SecureModelView(ModelView):
    def is_accessible(self):
        from flask_login import current_user
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for, flash
        flash("Bu sayfaya erişim izniniz yok!", "danger")
        return redirect(url_for('routes.login'))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .routes import routes
    app.register_blueprint(routes)

    with app.app_context():
        db.create_all()

    from .models import User, Post, Category, Comment

    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
    admin.add_view(SecureModelView(User, db.session))
    admin.add_view(SecureModelView(Post, db.session))
    admin.add_view(SecureModelView(Category, db.session))
    admin.add_view(SecureModelView(Comment, db.session))

    return app