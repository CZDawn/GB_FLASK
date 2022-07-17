import flask_admin
from flask import Flask, url_for
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import helpers as admin_helpers

from test_flask_lesson.config import Config
from test_flask_lesson.admin import MyModelView


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

def create_app():
    """Create an instance of Flask app (blueprint)"""

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    app.config['FLASK_ADMIN_SWATCH'] = 'Slate'
    app.config['BASIC_AUTH_USERNAME'] = 'admin'
    app.config['BASIC_AUTH_PASSWORD'] = '12345'
    
    from test_flask_lesson.main.routes import main
    from test_flask_lesson.users.routes import users
    from test_flask_lesson.posts.routes import posts
    from test_flask_lesson.errors.handlers import errors
    from test_flask_lesson.admin.routes import admin_bp
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from test_flask_lesson.models import User, Post, Comment, Like, Role

    admin = flask_admin.Admin(app, name='Blog', base_template='admin/my_master.html', template_mode='bootstrap3')

    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Post, db.session))
    admin.add_view(MyModelView(Comment, db.session))
    admin.add_view(MyModelView(Like, db.session))
    admin.add_view(MyModelView(Role, db.session))

    login_manager.login_view = 'admin_blueprint.login'
    
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    return app
